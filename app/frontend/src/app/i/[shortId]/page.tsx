import { motion } from "framer-motion";

interface PublicItem {
  short_id: string;
  title: string;
  description: string;
  tags: string[];
  location?: string | null;
  status: string;
  primary_image?: string | null;
}

async function getItem(shortId: string): Promise<PublicItem | null> {
  const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const res = await fetch(`${base}/i/${shortId}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function PublicItemPage({ params }: { params: { shortId: string } }) {
  const item = await getItem(params.shortId);

  if (!item) {
    return (
      <div className="flex h-full flex-col items-center justify-center text-center">
        <p className="text-xl font-semibold text-slate-800">Item not found</p>
        <p className="mt-2 text-sm text-slate-500">The label might be outdated. Contact the owner for details.</p>
      </div>
    );
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto flex w-full max-w-3xl flex-col gap-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-xl"
    >
      {item.primary_image ? (
        <motion.img
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.4 }}
          src={item.primary_image ?? ""}
          alt={item.title}
          className="h-64 w-full rounded-2xl object-cover"
        />
      ) : (
        <div className="flex h-64 items-center justify-center rounded-2xl bg-slate-100 text-slate-500">
          No image provided
        </div>
      )}

      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">{item.title}</h1>
          <p className="text-sm text-slate-500">#{item.short_id}</p>
        </div>
        <p className="text-base text-slate-600">{item.description}</p>
        <div className="flex flex-wrap gap-2">
          {item.tags.map((tag) => (
            <span key={tag} className="rounded-full bg-brand-500/10 px-3 py-1 text-sm text-brand-500">
              #{tag}
            </span>
          ))}
        </div>
        <div className="flex flex-col gap-2 text-sm text-slate-500">
          <span>Status: <strong className="text-slate-700">{item.status}</strong></span>
          <span>Location: <strong className="text-slate-700">{item.location ?? "Not specified"}</strong></span>
        </div>
        <div className="mt-4 rounded-2xl bg-slate-900/90 p-4 text-center text-sm text-white shadow-inner">
          <p>Share this item:</p>
          <p className="mt-1 font-mono text-xs">{`${process.env.NEXT_PUBLIC_PUBLIC_BASE ?? "http://localhost:5434"}/i/${item.short_id}`}</p>
        </div>
      </div>
    </motion.section>
  );
}
