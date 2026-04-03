/*
  Warnings:

  - You are about to drop the column `dropZones` on the `Shelf` table. All the data in the column will be lost.
  - Made the column `widthCm` on table `Shelf` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "Shelf" DROP COLUMN "dropZones",
ALTER COLUMN "widthCm" SET NOT NULL;
