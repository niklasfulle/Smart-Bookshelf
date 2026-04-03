import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const session = req.auth;

  const isAuthenticated = !!session?.user;
  const isAdmin = session?.user?.role === "ADMIN";

  // Redirect authenticated users away from auth pages
  if (isAuthenticated && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  // Protect all routes that require authentication
  const protectedPrefixes = ["/dashboard", "/bookshelves", "/books"];
  const isProtected = protectedPrefixes.some((prefix) => pathname.startsWith(prefix));
  if (!isAuthenticated && isProtected) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  // Admin-only routes
  if (pathname.startsWith("/admin") && !isAdmin) {
    if (!isAuthenticated) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    /*
     * Match all request paths except for:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     * - api/auth (NextAuth endpoints)
     */
    "/((?!_next/static|_next/image|favicon.ico|api/auth).*)",
  ],
};
