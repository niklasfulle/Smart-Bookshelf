import { z } from "zod";

// ---------------------------------------------------------------------------
// Task type constants (must match TASK_TYPES in ESP32_Server/utils/constants.py)
// ---------------------------------------------------------------------------

export const TASK_TYPE = {
  SLEEP: "task_sleep",
  REBOOT: "task_reboot",
  CONFIG_SEND: "task_config_send",
  CONFIG_REQUEST: "task_config_request",
  DATA_SEND_BOOK: "task_data_send_book",
  DATA_SEND_BOOKS: "task_data_send_books",
  DATA_SEND_MODE: "task_data_send_mode",
  DATA_SEND_LIGHT_ON: "task_data_send_ligh_on",
  DATA_SEND_LIGHT_OFF: "task_data_send_ligh_off",
} as const;

export type TaskType = (typeof TASK_TYPE)[keyof typeof TASK_TYPE];

export const taskTypeSchema = z.enum([
  TASK_TYPE.SLEEP,
  TASK_TYPE.REBOOT,
  TASK_TYPE.CONFIG_SEND,
  TASK_TYPE.CONFIG_REQUEST,
  TASK_TYPE.DATA_SEND_BOOK,
  TASK_TYPE.DATA_SEND_BOOKS,
  TASK_TYPE.DATA_SEND_MODE,
  TASK_TYPE.DATA_SEND_LIGHT_ON,
  TASK_TYPE.DATA_SEND_LIGHT_OFF,
]);

// ---------------------------------------------------------------------------
// Per-type data payload schemas
// The ESP32_Server reads `data` as a plain text string.
// Structured payloads are stored as JSON strings.
// ---------------------------------------------------------------------------

/** task_sleep: {"duration": <milliseconds>} */
const sleepDataSchema = z.object({
  duration: z.number().int().min(0).max(3_600_000),
});

/** task_config_send: raw config string passed verbatim to the device */
const configSendDataSchema = z.string().min(1, "Config data must not be empty");

/** task_data_send_book: single book position */
const bookDataSchema = z.object({
  shelving_unit: z.number().int().min(0),
  position: z.number().int().min(0),
});

/** task_data_send_books: array of book positions */
const booksDataSchema = z.array(bookDataSchema).min(1);

/** task_data_send_mode: bookshelf light mode */
const modeDataSchema = z.object({
  mode: z.enum(["books", "light", "sleep"]),
});

// ---------------------------------------------------------------------------
// Unified task creation schema (used by the web app)
// ---------------------------------------------------------------------------

export const createTaskSchema = z.object({
  type: taskTypeSchema,
  clientId: z.number().int().positive("Client ID must be a positive integer"),
  data: z.string().optional(),
});

export type CreateTaskInput = z.infer<typeof createTaskSchema>;

// ---------------------------------------------------------------------------
// Validates the `data` string for a given task type.
// ---------------------------------------------------------------------------

export function validateTaskData(
  type: TaskType,
  data: string | undefined | null,
): { success: true } | { success: false; error: string } {
  try {
    switch (type) {
      case TASK_TYPE.SLEEP: {
        const result = sleepDataSchema.safeParse(JSON.parse(data ?? "{}"));
        if (!result.success) return { success: false, error: result.error.message };
        break;
      }
      case TASK_TYPE.CONFIG_SEND: {
        const result = configSendDataSchema.safeParse(data);
        if (!result.success) return { success: false, error: result.error.message };
        break;
      }
      case TASK_TYPE.DATA_SEND_BOOK: {
        const result = bookDataSchema.safeParse(JSON.parse(data ?? "{}"));
        if (!result.success) return { success: false, error: result.error.message };
        break;
      }
      case TASK_TYPE.DATA_SEND_BOOKS: {
        const result = booksDataSchema.safeParse(JSON.parse(data ?? "[]"));
        if (!result.success) return { success: false, error: result.error.message };
        break;
      }
      case TASK_TYPE.DATA_SEND_MODE: {
        const result = modeDataSchema.safeParse(JSON.parse(data ?? "{}"));
        if (!result.success) return { success: false, error: result.error.message };
        break;
      }
      // No structured data needed for these task types
      case TASK_TYPE.REBOOT:
      case TASK_TYPE.CONFIG_REQUEST:
      case TASK_TYPE.DATA_SEND_LIGHT_ON:
      case TASK_TYPE.DATA_SEND_LIGHT_OFF:
        break;
    }
    return { success: true };
  } catch {
    return { success: false, error: "data is not valid JSON" };
  }
}


