import Link from "next/link";
import { motion } from "framer-motion";
import { Item } from "@/types";

interface ItemCardProps {
  item: Item;
}

export function ItemCard({ item }: ItemCardProps) {
  const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const primaryImage = item.images[0]?.path
    ? `${base}/media/${item.images[0].path}`
    : "https://placehold.co/400x300?text=No+Image";

  return (
    <motion.div
      whileHover={{ translateY: -4 }}
      className="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
    >
      <Link href={`/i/${item.short_id}`} className="block">
        <div className="relative h-48 w-full overflow-hidden">
          <img src={primaryImage} alt={item.title} className="h-full w-full object-cover transition duration-500 group-hover:scale-105" />
        </div>
        <div className="space-y-2 p-4">
          <h3 className="text-lg font-semibold text-slate-800">{item.title || "Untitled"}</h3>
          <p className="line-clamp-2 text-sm text-slate-500">{item.description}</p>
          <div className="flex flex-wrap gap-2">
            {(item.tags ?? []).map((tag) => (
              <span key={tag} className="rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-600">
                #{tag}
              </span>
            ))}
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
