"use client";

import { motion } from "framer-motion";
import { ItemSuggestions } from "@/types";

interface AiSuggestionBoxProps {
  suggestions: ItemSuggestions | null;
  onApply: (field: keyof ItemSuggestions, value: string | string[]) => void;
}

export function AiSuggestionBox({ suggestions, onApply }: AiSuggestionBoxProps) {
  if (!suggestions) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-500">
        AI suggestions will appear here.
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
    >
      <div>
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-700">Suggested title</h3>
          <button
            className="text-xs font-medium text-brand-500"
            onClick={() => onApply("title", suggestions.title)}
          >
            Use
          </button>
        </div>
        <p className="mt-1 text-sm text-slate-600">{suggestions.title}</p>
      </div>
      <div>
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-700">Suggested description</h3>
          <button
            className="text-xs font-medium text-brand-500"
            onClick={() => onApply("description", suggestions.description)}
          >
            Use
          </button>
        </div>
        <p className="mt-1 text-sm text-slate-600">{suggestions.description}</p>
      </div>
      <div>
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-700">Suggested tags</h3>
          <button
            className="text-xs font-medium text-brand-500"
            onClick={() => onApply("tags", suggestions.tags)}
          >
            Use
          </button>
        </div>
        <div className="mt-2 flex flex-wrap gap-2">
          {(suggestions.tags ?? []).map((tag) => (
            <span key={tag} className="rounded-full bg-brand-500/10 px-2 py-1 text-xs text-brand-500">
              #{tag}
            </span>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
