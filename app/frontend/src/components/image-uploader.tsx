"use client";

import { useCallback, useEffect, useState } from "react";

interface ImageUploaderProps {
  onFileSelected: (file: File) => void;
}

export function ImageUploader({ onFileSelected }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  const handleChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onFileSelected(file);
  }, [onFileSelected]);

  const handleDrop = useCallback((event: React.DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onFileSelected(file);
  }, [onFileSelected]);

  return (
    <label
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="flex h-40 w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-white text-center shadow-sm transition hover:border-brand-500 hover:bg-brand-50"
    >
      <input type="file" accept="image/*" className="hidden" onChange={handleChange} />
      {preview ? (
        <img src={preview} alt="Preview" className="h-full w-full rounded-lg object-cover" />
      ) : (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-slate-600">Drop an image or click to upload</p>
          <p className="text-xs text-slate-500">Supports camera input on mobile</p>
        </div>
      )}
    </label>
  );
}
