"use client";

import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { useRouter } from "next/navigation";
import { useAppContext } from "@/contexts/AppContext";
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  useDroppable,
  useDraggable,
  pointerWithin,
  type DragStartEvent,
  type DragEndEvent,
  type DragOverEvent,
} from "@dnd-kit/core";
import Image from "next/image";
import type { BookshelfWithShelves, ShelfWithPlacements } from "@/features/bookshelves/service";

type Placement = ShelfWithPlacements["placements"][number];

interface ShelfState {
  id: string;
  order: number;
  name: string | null;
  placements: Placement[];
  widthCm: number; // Required: used to calculate dropZones
}

interface BookshelfDndProps {
  bookshelf: BookshelfWithShelves;
  shelfLabel: string;
  noBooks: string;
  noShelvesVisual: string;
}

const DEFAULT_THICKNESS_PX = 28;
const DEFAULT_HEIGHT_PX = 150;
const BOARD_HEIGHT_PX = 12;
const CM_TO_PX = 14;
const BOOK_WIDTH_CM = 3.5; // Each book is 3.5cm wide

function darkenHex(hex: string, amount: number): string {
  const n = Number.parseInt(hex.replaceAll("#", ""), 16);
  const r = Math.max(0, (n >> 16) - amount);
  const g = Math.max(0, ((n >> 8) & 0xff) - amount);
  const b = Math.max(0, (n & 0xff) - amount);
  return `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
}

// ── Single draggable + droppable spine ──────────────────────────────────────

interface SpineProps {
  placement: Placement;
  shelfId: string;
  anyDragging: boolean;
  isOverlay?: boolean;
  editMode?: boolean;
}

function BookSpineItem({ placement, shelfId, anyDragging, isOverlay = false, editMode = false }: Readonly<SpineProps>) {
  const [hovered, setHovered] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const router = useRouter();
  const { t } = useAppContext();
  const { book } = placement.userBook;

  const color = book.spineColor ?? "#6b7280";
  const edgeColor = darkenHex(color.startsWith("#") ? color : "#6b7280", 40);
  
  // Each book is always BOOK_WIDTH_CM wide (one zone)
  const widthPx = BOOK_WIDTH_CM * CM_TO_PX;
  
  const heightPx = book.heightCm ? Math.max(80, book.heightCm * CM_TO_PX) : DEFAULT_HEIGHT_PX;
  const coverWidthPx = Math.round(heightPx * 0.65);
  const authorDisplay = book.authors.slice(0, 1).join(", ");

  // Draggable
  const {
    attributes,
    listeners,
    setNodeRef: setDragRef,
    transform,
    isDragging,
  } = useDraggable({
    id: placement.id,
    disabled: isOverlay || !editMode,
    data: { shelfId },
  });

  const translateX = transform?.x ?? 0;
  const translateY = transform?.y ?? 0;

  const handleDeleteConfirm = async () => {
    setIsDeleting(true);
    try {
      const res = await fetch(`/api/placements/${placement.id}/delete`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Delete failed");
      // Close the modal and notify parent to remove the placement immediately
      setShowDeleteConfirm(false);
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("placement-removed", { detail: { id: placement.id, shelfId: placement.shelfId } }));
      }
      // Refresh in background to keep server state in sync
      router.refresh();
    } catch (error) {
      console.error("Error deleting placement:", error);
      setShowDeleteConfirm(false);
      alert(t.bookshelves.failedDeletePlacement);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      ref={setDragRef}
      style={{
        transform: isDragging ? undefined : `translate(${translateX}px,${translateY}px)`,
        opacity: isDragging ? 0.2 : 1,
        width: widthPx,
        height: heightPx,
        position: "relative",
        flexShrink: 0,
        zIndex: hovered ? 50 : undefined,
        borderRadius: "2px",
      }}
      {...attributes}
      {...listeners}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => {
        setHovered(false);
      }}
      className="cursor-grab active:cursor-grabbing select-none group relative"
    >
      {/* Delete Button - Show only in edit mode */}
      {hovered && !anyDragging && editMode && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowDeleteConfirm(true);
            }}
            className="absolute top-1 left-1 z-[200] p-1 rounded bg-red-500 hover:bg-red-600 text-white shadow-lg transition-all opacity-100 animate-in fade-in duration-200"
            title={t.bookshelves.removeFromShelfTitle}
          >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}

      {/* Delete Confirmation Modal - rendered via portal to avoid overflow clipping */}
      {showDeleteConfirm && typeof document !== 'undefined' && createPortal(
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={() => !isDeleting && setShowDeleteConfirm(false)}>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-sm mx-4 border border-gray-200 dark:border-gray-700" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 dark:bg-red-900/30">
                <svg className="h-6 w-6 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4v2m0 0H9m3 0h3m-6-4h12a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  {book.title}
                </h3>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  {t.bookshelves.confirmRemovePlacement}
                </p>
              </div>
            </div>
            <div className="mt-6 flex gap-3 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                disabled={isDeleting}
                className="px-4 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
              >
                {t.bookshelves.cancel}
              </button>
              <button
                onClick={handleDeleteConfirm}
                disabled={isDeleting}
                className="px-4 py-2 rounded-lg text-sm font-medium text-white bg-red-600 hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isDeleting ? t.bookshelves.removing : t.bookshelves.remove}
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}

      {/* Cover popup */}
      {hovered && !anyDragging && (
        <div
          className="pointer-events-none absolute overflow-hidden rounded shadow-2xl border border-gray-200 dark:border-gray-700"
          style={{
            width: coverWidthPx,
            height: heightPx,
            bottom: 0,
            left: 0,
            zIndex: 100,
          }}
        >
          {book.coverImageUrl ? (
            <Image
              src={book.coverImageUrl}
              alt={book.title}
              width={coverWidthPx}
              height={heightPx}
              className="h-full w-full object-cover"
              unoptimized
            />
          ) : (
            <div
              className="flex h-full w-full flex-col items-center justify-center gap-1 p-2 text-center"
              style={{ backgroundColor: color }}
            >
              <span className="text-xs font-semibold leading-tight text-white">{book.title}</span>
              {authorDisplay && <span className="text-xs text-white/70">{authorDisplay}</span>}
            </div>
          )}
        </div>
      )}

      {/* Spine face */}
      <div
        className="absolute inset-0 flex items-center justify-center overflow-hidden rounded-sm"
        style={{
          background: `linear-gradient(to right, ${edgeColor} 0%, ${color} 8%, ${color} 92%, ${edgeColor} 100%)`,
          boxShadow: isOverlay ? "4px 6px 20px rgba(0,0,0,0.5)" : "1px 0 4px rgba(0,0,0,0.2)",
          transform: isOverlay ? "rotate(-4deg) scale(1.06)" : undefined,
        }}
      >
        <div
          style={{
            writingMode: "vertical-rl",
            transform: "rotate(180deg)",
            overflow: "hidden",
            maxHeight: heightPx - 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
            padding: "0 2px",
          }}
        >
          <span
            className="truncate font-semibold leading-tight text-white drop-shadow"
            style={{ fontSize: Math.min(11, Math.max(8, widthPx * 0.35)) }}
          >
            {book.title}
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

// ── Shelf row — dynamic zones for positioning ──────────────────────────────

function ShelfRow({
  shelf,
  shelfLabel,
  noBooks,
  anyDragging,
  editMode,
}: Readonly<{
  shelf: ShelfState;
  shelfLabel: string;
  noBooks: string;
  anyDragging: boolean;
  editMode?: boolean;
}>) {
  const label = shelf.name ?? `${shelfLabel} ${shelf.order}`;
  const rowHeight = DEFAULT_HEIGHT_PX + BOARD_HEIGHT_PX + 24;
  
  // Calculate zones from shelf width (1 zone = 4cm book width)
  const dropZones = calculateDropZones(shelf.widthCm);
  const zoneWidth = 100 / dropZones; // Each zone takes equal width

  // Create drop zones - one for each zone
  
  // Individual drop zone component (calls hook at top-level of a component)
  function DropZone({
    shelf,
    zoneIndex,
    zoneWidth,
    dropZones,
    anyDragging,
    editMode,
  }: Readonly<{
    shelf: ShelfState;
    zoneIndex: number;
    zoneWidth: number;
    dropZones: number;
    anyDragging: boolean;
    editMode?: boolean;
  }>) {
    const { setNodeRef, isOver } = useDroppable({
      id: `zone-${shelf.id}-${zoneIndex}`,
      data: { type: "zone", shelfId: shelf.id, zoneIndex, dropZones },
    });

    const { start, end } = getPositionsForZone(zoneIndex);
    const booksInZone = shelf.placements.filter((p) => p.position >= start && p.position < end);

    return (
      <div
        ref={setNodeRef}
        className="absolute top-0 bottom-[12px] flex items-end px-1"
        style={{
          left: `${zoneIndex * zoneWidth}%`,
          width: `${zoneWidth}%`,
          backgroundColor: isOver && anyDragging ? "rgba(99, 102, 241, 0.15)" : "transparent",
          transition: "background-color 150ms ease",
          borderRight: anyDragging ? "1px solid rgba(99, 102, 241, 0.3)" : "none",
        }}
      >
        {/* Show books that belong to this zone */}
        {booksInZone.length > 0 && (
          <div className="flex items-end gap-0">
            {booksInZone.map((p) => (
              <BookSpineItem
                key={p.id}
                placement={p}
                shelfId={shelf.id}
                anyDragging={anyDragging}
                editMode={editMode}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="flex items-center gap-4 mb-2">
      {/* Vertical shelf label on the left to save vertical space between shelf levels */}
      <div className="flex items-center justify-center" style={{ width: 32 }}>
        <span
          className="text-xs font-medium text-gray-400 dark:text-gray-500"
          style={{ writingMode: "vertical-rl", transform: "rotate(180deg)", whiteSpace: "nowrap" }}
        >
          {label}
        </span>
      </div>

      <div className="relative overflow-x-clip overflow-y-visible flex-1" style={{ height: rowHeight }}>
        {/* Render each drop zone via DropZone component to obey Hooks rules */}
        {Array.from({ length: dropZones }).map((_, zoneIndex) => (
          <DropZone
            key={zoneIndex}
            shelf={shelf}
            zoneIndex={zoneIndex}
            zoneWidth={zoneWidth}
            dropZones={dropZones}
            anyDragging={anyDragging}
            editMode={editMode}
          />
        ))}

        {/* Show empty state across full width when no books */}
        {shelf.placements.length === 0 && (
          <div
            className="absolute top-0 bottom-[12px] left-0 right-0 flex items-center justify-center"
          >
            <div
              className="flex w-full h-full items-center justify-center rounded border-2 border-dashed transition-colors border-gray-200 text-gray-400 dark:border-gray-600 dark:text-gray-500"
            >
              <span className="text-sm">{noBooks}</span>
            </div>
          </div>
        )}

        {/* Shelf board */}
        <div
          className="absolute right-0 bottom-0 left-0 rounded-sm"
          style={{
            height: BOARD_HEIGHT_PX,
            background: "linear-gradient(to bottom, #c8a96e 0%, #b08040 40%, #8b5e20 100%)",
            boxShadow: "0 2px 4px rgba(0,0,0,0.25)",
          }}
        />
      </div>
    </div>
  );
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function compactShelf(s: ShelfState): ShelfState {
  return { ...s, placements: s.placements.map((p, i) => ({ ...p, position: i })) };
}

/**
 * Get positions that belong to a zone
 * Position directly maps to zone: zone N contains books with position N
 */
function getPositionsForZone(zoneIndex: number): { start: number; end: number } {
  return { start: zoneIndex, end: zoneIndex + 1 };
}

/**
 * Calculate number of zones from shelf width in cm
 * 1 zone = 4cm (book width)
 */
function calculateDropZones(widthCm: number): number {
  return Math.max(1, Math.floor(widthCm / BOOK_WIDTH_CM));
}

/**
 * Calculate zone width in pixels from width in cm
 */
function calculateZoneWidthPx(widthCm: number): number {
  const CM_TO_PX = 14; // Same as global constant
  return (widthCm * CM_TO_PX) / calculateDropZones(widthCm);
}

function buildShelves(bookshelf: BookshelfWithShelves): ShelfState[] {
  return [...bookshelf.shelves]
    .sort((a, b) => a.order - b.order)
    .map((s) => ({
      id: s.id,
      order: s.order,
      name: s.name,
      widthCm: s.widthCm || 80, // Fallback if somehow missing
      placements: [...s.placements].sort((a, b) => a.position - b.position),
    }));
}

// ── Main export ──────────────────────────────────────────────────────────────

export function BookshelfDnd({
  bookshelf,
  shelfLabel,
  noBooks,
  noShelvesVisual,
}: Readonly<BookshelfDndProps>) {
  const router = useRouter();
  const { t } = useAppContext();
  const [shelves, setShelves] = useState<ShelfState[]>(() => buildShelves(bookshelf));
  const [activePlacement, setActivePlacement] = useState<Placement | null>(null);
  const [editMode, setEditMode] = useState(false);
  const shelvesRef = useRef(shelves);
  const targetPlacementIdRef = useRef<string | undefined>(undefined);
  shelvesRef.current = shelves;

  // Placement add/remove listeners are registered below

  useEffect(() => {
    const handlePlacementAdded = (event: Event) => {
      const customEvent = event as CustomEvent<{ placement: Placement }>;
      const placement = customEvent.detail.placement;
      
      setShelves((prev) => {
        const next = prev.map((s) => ({ ...s, placements: [...s.placements] }));
        const targetShelf = next.find((s) => s.id === placement.shelfId);
        if (targetShelf && !targetShelf.placements.some((p) => p.id === placement.id)) {
          targetShelf.placements.push(placement);
          targetShelf.placements.sort((a, b) => a.position - b.position);
        }
        return next;
      });
    };

    const handlePlacementRemoved = (event: Event) => {
      const customEvent = event as CustomEvent<{ id: string; shelfId?: string }>;
      const removedId = customEvent.detail.id;
      const shelfId = customEvent.detail.shelfId;

      setShelves((prev) => {
        const next = prev.map((s) => ({ ...s, placements: [...s.placements] }));
        if (shelfId) {
          const target = next.find((s) => s.id === shelfId);
          if (target) {
            target.placements = target.placements.filter((p) => p.id !== removedId);
          }
        } else {
          // Remove from any shelf that contains it
          for (const s of next) {
            s.placements = s.placements.filter((p) => p.id !== removedId);
          }
        }
        return next;
      });
    };

    window.addEventListener('placement-added', handlePlacementAdded);
    window.addEventListener('placement-removed', handlePlacementRemoved);
    return () => {
      window.removeEventListener('placement-added', handlePlacementAdded);
      window.removeEventListener('placement-removed', handlePlacementRemoved);
    };
  }, []);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
  );

  function findShelfId(placementId: string): string | undefined {
    return shelves.find((s) => s.placements.some((p) => p.id === placementId))?.id;
  }

  function findPlacement(placementId: string): Placement | undefined {
    for (const s of shelves) {
      const found = s.placements.find((p) => p.id === placementId);
      if (found) return found;
    }
    return undefined;
  }

  function handleDragStart(event: DragStartEvent) {
    setActivePlacement(findPlacement(String(event.active.id)) ?? null);
  }

  function handleDragOver(event: DragOverEvent) {
    const activeId = String(event.active.id);
    const over = event.over;
    if (!over) return;

    const fromShelfId = findShelfId(activeId);
    const overData = over.data.current as { 
      type?: string; 
      shelfId?: string;
      zoneIndex?: number;
      dropZones?: number;
    } | undefined;

    if (!overData?.type || overData.type !== "zone" || !overData?.shelfId) return;
    
    const toShelfId = overData.shelfId;
    const zoneIndex = overData.zoneIndex ?? 0;
    
    if (!fromShelfId) return;

    // Check if moving to same shelf - if so, check if position is already occupied
    if (fromShelfId === toShelfId) {
      const toShelf = shelves.find(s => s.id === toShelfId);
      if (toShelf) {
        const targetBook = toShelf.placements.find(p => p.position === zoneIndex);
        const movingBook = toShelf.placements.find(p => p.id === activeId);
        
        // If position is occupied by a DIFFERENT book, don't update (can't place on occupied position)
        if (targetBook && targetBook.id !== activeId) {
          console.log("[handleDragOver] Position occupied, skipping optimistic update");
          return;
        }
      }
    }

    // Run optimistic update - just move the book
    setShelves((prev) => {
      const next = prev.map((s) => ({ ...s, placements: [...s.placements] }));
      const from = next.find((s) => s.id === fromShelfId);
      const to = next.find((s) => s.id === toShelfId);
      if (!from || !to) return prev;
      
      const idx = from.placements.findIndex((p) => p.id === activeId);
      if (idx === -1) return prev;

      const [moved] = from.placements.splice(idx, 1);
      moved.position = zoneIndex;
      
      to.placements.push(moved);
      to.placements.sort((a, b) => a.position - b.position);
      
      return next;
    });

    }

    async function handleDragEnd(event: DragEndEvent) {
      const activeId = String(event.active.id);
      setActivePlacement(null);

      const over = event.over;
      if (!over) return;

      const overData = over.data.current as { 
        type?: string; 
        shelfId?: string; 
        zoneIndex?: number;
        dropZones?: number;
      } | undefined;
      if (!overData?.shelfId || overData.type !== "zone") return;

      const shelfId = overData.shelfId;
      const zoneIndex = overData.zoneIndex ?? 0;
      const targetPosition = zoneIndex;

      console.log("[handleDragEnd] Zone drop:", { 
        activeId, 
        shelfId, 
        zoneIndex, 
        targetPosition,
      });

      try {
        const res = await fetch(`/api/placements/${activeId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            shelfId, 
            position: targetPosition,
          }),
        });
        
        if (!res.ok) {
          const errorData = await res.json();
          console.error("[handleDragEnd] API error:", { status: res.status, error: errorData });
          // Error - revert to server state
          router.refresh();
          return;
        }
        
        const responseData = await res.json();
        console.log("[handleDragEnd] Success:", responseData);
        
        // Check if placement was already optimistically updated
        const fromShelfId = findShelfId(activeId);
        const alreadyInShelves = fromShelfId !== undefined;
        
        if (!alreadyInShelves && responseData?.placement) {
          // Placement came from outside (e.g., Collection)
          // Add it to the target shelf in the local state
          const placement = responseData.placement;
          setShelves((prev) => {
            const next = prev.map((s) => ({ ...s, placements: [...s.placements] }));
            const targetShelf = next.find((s) => s.id === shelfId);
            if (targetShelf && !targetShelf.placements.some((p) => p.id === placement.id)) {
              targetShelf.placements.push(placement);
              targetShelf.placements.sort((a, b) => a.position - b.position);
            }
            return next;
          });
        }
        
        // Refresh in background to keep server state in sync
        router.refresh();
      } catch (error) {
        console.error("[handleDragEnd] Error:", error);
        // Network error - revert state
        router.refresh();
      }
    }

  if (bookshelf.shelves.length === 0) {
    return (
      <div className="flex min-h-[200px] w-full flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed border-gray-200 p-8 text-center dark:border-gray-700">
        <p className="text-sm text-gray-500 dark:text-gray-400">{noShelvesVisual}</p>
      </div>
    );
  }

  return (
    <DndContext
      id="bookshelf-dnd"
      sensors={sensors}
      collisionDetection={pointerWithin}
      onDragStart={handleDragStart}
      onDragOver={handleDragOver}
      onDragEnd={(e) => void handleDragEnd(e)}
    >
      <div className="w-full">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {editMode ? t.bookshelves.editModeActive : t.bookshelves.viewArrangement}
          </h3>
          <button
            onClick={() => setEditMode(!editMode)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              editMode
                ? "bg-indigo-600 text-white hover:bg-indigo-700"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
            }`}
          >
            {editMode ? t.bookshelves.doneEditing : t.bookshelves.edit}
          </button>
        </div>

        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-amber-50 p-6 shadow-inner dark:border-gray-700 dark:bg-amber-950/20">
          <div className="flex min-w-max flex-col gap-2">
            {shelves.map((shelf) => (
              <ShelfRow
                key={shelf.id}
                shelf={shelf}
                shelfLabel={shelfLabel}
                noBooks={noBooks}
                anyDragging={activePlacement !== null}
                editMode={editMode}
              />
            ))}
          </div>
        </div>
      </div>

      <DragOverlay dropAnimation={null}>
        {activePlacement && (
          <BookSpineItem
            placement={activePlacement}
            shelfId=""
            anyDragging
            isOverlay
            editMode={editMode}
          />
        )}
      </DragOverlay>
    </DndContext>
  );
}
