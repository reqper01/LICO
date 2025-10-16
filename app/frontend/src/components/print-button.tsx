"use client";

import { useState } from "react";

interface PrintButtonProps {
  itemId: string;
}

const SIZE_OPTIONS = [
  { label: "50 × 30 mm", value: "50x30" },
  { label: "40 × 30 mm", value: "40x30" },
  { label: "62 × 30 mm", value: "62x30" },
];

export function PrintButton({ itemId }: PrintButtonProps) {
  const [size, setSize] = useState("50x30");
  const [copies, setCopies] = useState(1);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handlePrint = async () => {
    setLoading(true);
    const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
    try {
      const response = await fetch(`${base}/api/items/${itemId}/print`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ size, copies }),
      });
      const json = await response.json();
      if (!response.ok) {
        throw new Error(json.detail ?? "Failed to queue print job");
      }
      setStatus(`Queued job ${json.job_id}`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : "Failed to queue print job");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium text-slate-600">Label size</label>
        <select
          value={size}
          onChange={(event) => setSize(event.target.value)}
          className="rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
        >
          {SIZE_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <input
          type="number"
          min={1}
          max={20}
          value={copies}
          onChange={(event) => setCopies(Number(event.target.value))}
          className="w-20 rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
        />
      </div>
      <button
        onClick={handlePrint}
        disabled={loading}
        className="w-full rounded-full bg-brand-500 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-slate-300"
      >
        {loading ? "Sending to printer..." : "Print label"}
      </button>
      {status && <p className="text-xs text-slate-500">{status}</p>}
    </div>
  );
}
