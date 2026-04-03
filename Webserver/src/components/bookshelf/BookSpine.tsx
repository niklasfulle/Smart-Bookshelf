"use client";

import { useState } from "react";
import Image from "next/image";

export interface BookSpineProps {
  title: string;
  authors: string[];
  spineColor?: string | null;
  coverImageUrl?: string | null;
  /** Thickness in cm; falls back to a default if not provided */
  thicknessCm?: number | null;
  heightCm?: number | null;
}

const DEFAULT_THICKNESS_PX = 28;
const DEFAULT_HEIGHT_PX = 160;
const CM_TO_PX = 14; // 1 cm ≈ 14 px for shelf rendering

/** Darkens a hex color by the given amount (0–255) for the spine shadow edge. */
function darkenHex(hex: string, amount: number): string {
  const n = Number.parseInt(hex.replaceAll("#", ""), 16);
  const r = Math.max(0, (n >> 16) - amount);
  const g = Math.max(0, ((n >> 8) & 0xff) - amount);
  const b = Math.max(0, (n & 0xff) - amount);
  return `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
}

/**
 * Renders a single book as a spine block.
 *
 * On hover:
 * - The spine tilts away from the viewer (rotateY pivot on left edge)
 *   giving the impression of turning toward the cover side.
 * - The cover card slides in from above with a fade transition.
 *
 * overflow-x-clip on the parent ShelfLevel keeps overflow-y truly
 * visible so the cover card above the shelf is never clipped.
 */
export function BookSpine({
  title,
  authors,
  spineColor,
  coverImageUrl,
  thicknessCm,
  heightCm,
}: BookSpineProps) {
  const [hovered, setHovered] = useState(false);

  const color = spineColor ?? "#6b7280";
  const edgeColor = darkenHex(color.startsWith("#") ? color : "#6b7280", 40);

  const widthPx = thicknessCm ? Math.max(16, thicknessCm * CM_TO_PX) : DEFAULT_THICKNESS_PX;
  const heightPx = heightCm ? Math.max(80, heightCm * CM_TO_PX) : DEFAULT_HEIGHT_PX;
  // Cover proportions: typical book cover ~0.65×height
  const coverWidthPx = Math.round(heightPx * 0.65);

  const authorDisplay = authors.slice(0, 1).join(", ");

  return (
    <div
      className="relative flex-shrink-0 cursor-pointer select-none"
      style={{
        width: widthPx,
        height: heightPx,
        perspective: "500px",
        zIndex: hovered ? 50 : undefined,
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {/* ── Cover preview ──
           Positioned above the spine. Visible because ShelfLevel uses
           overflow-x-clip (not overflow-x-auto), which keeps overflow-y
           truly visible per CSS spec. */}
      <div
        className="pointer-events-none absolute overflow-hidden rounded shadow-xl"
        style={{
          width: coverWidthPx,
          height: heightPx,
          bottom: `calc(100% + 6px)`,
          left: `${Math.round((widthPx - coverWidthPx) / 2)}px`,
          opacity: hovered ? 1 : 0,
          transform: hovered ? "translateY(0) scale(1)" : "translateY(12px) scale(0.95)",
          transition: "opacity 0.3s ease, transform 0.3s ease",
        }}
      >
        {coverImageUrl ? (
          <Image
            src={coverImageUrl}
            alt={`Cover: ${title}`}
            width={coverWidthPx}
            height={heightPx}
            className="h-full w-full object-cover"
            unoptimized
          />
        ) : (
          <div
            className="flex h-full w-full flex-col items-center justify-center gap-2 p-3 text-center"
            style={{ backgroundColor: color }}
          >
            <span className="text-xs font-semibold leading-tight text-white">{title}</span>
            {authorDisplay && (
              <span className="text-xs text-white/70">{authorDisplay}</span>
            )}
          </div>
        )}
      </div>

      {/* ── Spine ──
           Tilts on the left edge (spine binding) toward the viewer on hover,
           like a book being pulled open off a shelf. */}
      <div
        className="absolute inset-0 flex items-center justify-center overflow-hidden rounded-sm"
        style={{
          background: `linear-gradient(to right, ${edgeColor} 0%, ${color} 8%, ${color} 92%, ${edgeColor} 100%)`,
          boxShadow: hovered
            ? `3px 0 14px rgba(0,0,0,0.45), -1px 0 0 rgba(0,0,0,0.12)`
            : `1px 0 4px rgba(0,0,0,0.2)`,
          transformOrigin: "left center",
          transform: hovered ? "rotateY(-40deg) translateY(-3px)" : "rotateY(0deg)",
          transition: "transform 0.35s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.35s ease",
        }}
      >
        <div
          className="flex flex-col items-center gap-0.5 px-0.5"
          style={{
            writingMode: "vertical-rl",
            transform: "rotate(180deg)",
            overflow: "hidden",
            maxHeight: heightPx - 8,
          }}
        >
          <span
            className="truncate font-semibold leading-tight text-white drop-shadow"
            style={{ fontSize: Math.min(11, Math.max(8, widthPx * 0.35)) }}
          >
            {title}
          </span>
          {widthPx >= 22 && (
            <span
              className="truncate leading-tight text-white/70"
              style={{ fontSize: Math.min(9, Math.max(7, widthPx * 0.28)) }}
            >
              {authorDisplay}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
