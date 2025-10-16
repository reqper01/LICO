"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { AiSuggestionBox } from "@/components/ai-suggestion-box";
import { ImageUploader } from "@/components/image-uploader";
import { PrintButton } from "@/components/print-button";
import { QrPreview } from "@/components/qr-preview";
import { Item, ItemSuggestions } from "@/types";

interface FormState {
  title: string;
  description: string;
  tags: string;
  textHint: string;
  location: string;
}

const initialState: FormState = {
  title: "",
  description: "",
  tags: "",
  textHint: "",
  location: "",
};

export default function NewItemPage() {
  const router = useRouter();
  const [form, setForm] = useState<FormState>(initialState);
  const [image, setImage] = useState<File | null>(null);
  const [item, setItem] = useState<Item | null>(null);
  const [suggestions, setSuggestions] = useState<ItemSuggestions | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleInputChange = (field: keyof FormState, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleCreate = async () => {
    setLoading(true);
    setMessage(null);
    const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
    const formData = new FormData();
    formData.set("title", form.title);
    formData.set("description", form.description);
    formData.set(
      "tags",
      JSON.stringify(
        form.tags
          .split(",")
          .map((tag) => tag.trim())
          .filter(Boolean)
      )
    );
    formData.set("location", form.location);
    formData.set("text_hint", form.textHint);
    if (image) {
      formData.set("image", image);
    }

    try {
      const response = await fetch(`${base}/api/items/`, {
        method: "POST",
        body: formData,
      });
      const json = await response.json();
      if (!response.ok) {
        throw new Error(json.detail ?? "Failed to create item");
      }
      setItem(json.item);
      setForm((prev) => ({
        ...prev,
        title: json.item.title ?? "",
        description: json.item.description ?? "",
        tags: Array.isArray(json.item.tags) ? json.item.tags.join(", ") : prev.tags,
        location: json.item.location ?? "",
      }));
      setSuggestions(json.suggestions);
      setMessage("Item created! Review suggestions below.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to create item");
    } finally {
      setLoading(false);
    }
  };

  const applySuggestion = async (field: keyof ItemSuggestions, value: string | string[]) => {
    if (!item) return;
    const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
    const payload: Record<string, unknown> = { [field]: value };

    try {
      const response = await fetch(`${base}/api/items/${item.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const json = await response.json();
      if (!response.ok) {
        throw new Error(json.detail ?? "Failed to update item");
      }
      setItem(json);
      if (field === "title" || field === "description") {
        setForm((prev) => ({ ...prev, [field]: value as string }));
      }
      if (field === "tags") {
        setForm((prev) => ({ ...prev, tags: (value as string[]).join(", ") }));
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Failed to apply suggestion");
    }
  };

  return (
    <div className="grid gap-8 md:grid-cols-[2fr,1fr]">
      <div className="space-y-6">
        <div>
          <button onClick={() => router.push("/")} className="text-sm text-brand-500">
            ← Back to list
          </button>
          <h1 className="mt-2 text-3xl font-bold text-slate-900">New item</h1>
          <p className="text-sm text-slate-500">Upload a photo, add notes and generate a QR label.</p>
        </div>

        <ImageUploader onFileSelected={setImage} />

        <div className="space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <label className="text-sm font-medium text-slate-600">Title</label>
            <input
              value={form.title}
              onChange={(event) => handleInputChange("title", event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-600">Description</label>
            <textarea
              rows={4}
              value={form.description}
              onChange={(event) => handleInputChange("description", event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-600">Tags</label>
            <input
              value={form.tags}
              onChange={(event) => handleInputChange("tags", event.target.value)}
              placeholder="Comma separated"
              className="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-600">Location</label>
            <input
              value={form.location}
              onChange={(event) => handleInputChange("location", event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-slate-600">Text hint for AI</label>
            <textarea
              rows={3}
              value={form.textHint}
              onChange={(event) => handleInputChange("textHint", event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleCreate}
            disabled={loading}
            className="rounded-full bg-brand-500 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {loading ? "Creating..." : "Save & suggest"}
          </button>
        </div>
        {message && <p className="text-sm text-slate-500">{message}</p>}

        {item && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid gap-6 md:grid-cols-2">
            <QrPreview itemId={item.id} shortId={item.short_id} />
            <PrintButton itemId={item.id} />
          </motion.div>
        )}
      </div>

      <div className="space-y-4">
        <AiSuggestionBox suggestions={suggestions} onApply={applySuggestion} />
      </div>
    </div>
  );
}
