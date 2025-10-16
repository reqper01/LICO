"use client";

import { useMemo } from "react";

interface QrPreviewProps {
  itemId: string;
  shortId: string;
}

export function QrPreview({ itemId, shortId }: QrPreviewProps) {
  const qrUrl = useMemo(() => {
    const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
    return `${base}/api/items/${itemId}/qr.png`;
  }, [itemId]);

  const publicUrl = `${process.env.NEXT_PUBLIC_PUBLIC_BASE ?? "http://localhost:5434"}/i/${shortId}`;

  return (
    <div className="flex flex-col items-center gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <img src={qrUrl} alt="QR code" className="h-40 w-40" />
      <div className="text-center text-sm text-slate-600">
        <p className="font-semibold">Scan to open item page</p>
        <p className="mt-1 break-all text-xs text-slate-500">{publicUrl}</p>
      </div>
    </div>
  );
}
