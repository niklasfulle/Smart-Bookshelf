"use server";

import bcryptjs from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { signIn } from "@/lib/auth";
import { registerSchema, loginSchema } from "./schemas";
import { type Result, ok, err, conflict, internalError } from "@/lib/errors";
import { AuthError } from "next-auth";

const BCRYPT_ROUNDS = 12;

export async function registerUser(
  formData: FormData,
): Promise<Result<{ id: string; email: string }>> {
  const raw = {
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
    confirmPassword: formData.get("confirmPassword"),
  };

  const parsed = registerSchema.safeParse(raw);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid registration data",
      issues: parsed.error.flatten().fieldErrors as Record<string, string[]>,
    });
  }

  const { name, email, password } = parsed.data;

  const existing = await prisma.user.findUnique({ where: { email } });
  if (existing) {
    return err(conflict("An account with this email already exists"));
  }

  const passwordHash = await bcryptjs.hash(password, BCRYPT_ROUNDS);

  try {
    const user = await prisma.user.create({
      data: { name, email, passwordHash },
      select: { id: true, email: true },
    });
    return ok(user);
  } catch {
    return err(internalError("Failed to create account"));
  }
}

export async function loginUser(formData: FormData): Promise<Result<void>> {
  const raw = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const parsed = loginSchema.safeParse(raw);
  if (!parsed.success) {
    return err({
      type: "VALIDATION_ERROR",
      message: "Invalid credentials",
    });
  }

  try {
    await signIn("credentials", {
      email: parsed.data.email,
      password: parsed.data.password,
      redirectTo: "/dashboard",
    });
    return ok(undefined);
  } catch (e) {
    if (e instanceof AuthError) {
      return err({ type: "UNAUTHORIZED", message: "Invalid email or password" });
    }
    // signIn with redirectTo throws a NEXT_REDIRECT which must propagate.
    throw e;
  }
}
