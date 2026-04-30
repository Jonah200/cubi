import type { Solve } from '@/api/models'

export const mockSolves: Solve[] = [
  { id: 'a1b2c3d4-0001-4000-8000-000000000010', solveNo: 10, scramble: "R U R' U' R' F R2 U' R' U' R U R' F'", solveTime: 12.34, createdAt: '2026-04-16T10:30:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000009', solveNo: 9, scramble: "F R U' R' U' R U R' F' R U R' U' R' F R F'", solveTime: 14.21, createdAt: '2026-04-16T10:25:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000008', solveNo: 8, scramble: "U R U' R' U' F R F'", solveTime: 11.87, createdAt: '2026-04-16T10:20:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000007', solveNo: 7, scramble: "R U R' U R U2 R'", solveTime: 13.45, createdAt: '2026-04-16T10:15:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000006', solveNo: 6, scramble: "R' U' R U' R' U2 R", solveTime: 15.02, createdAt: '2026-04-16T10:10:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000005', solveNo: 5, scramble: "F R U R' U' F'", solveTime: 10.98, createdAt: '2026-04-16T10:05:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000004', solveNo: 4, scramble: "R U R' U' R' F R2 U' R' U R U R' F'", solveTime: 16.73, createdAt: '2026-04-16T10:00:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000003', solveNo: 3, scramble: "U R U' R' U' F R F'", solveTime: 12.05, createdAt: '2026-04-15T22:00:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000002', solveNo: 2, scramble: "R U2 R' U' R U' R'", solveTime: 14.56, createdAt: '2026-04-15T21:55:00Z' },
  { id: 'a1b2c3d4-0001-4000-8000-000000000001', solveNo: 1, scramble: "F R U' R' U' R U R' F'", solveTime: 18.32, createdAt: '2026-04-15T21:50:00Z' },
]
