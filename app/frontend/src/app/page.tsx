import Link from "next/link";
import { ItemCard } from "@/components/item-card";
import { Item } from "@/types";

async function getItems(search?: string): Promise<Item[]> {
  const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const params = new URLSearchParams();
  if (search) params.set("search", search);
  const res = await fetch(`${base}/api/items?${params.toString()}`, { cache: "no-store" });
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export default async function Home({ searchParams }: { searchParams?: { q?: string } }) {
  const items = await getItems(searchParams?.q);

  return (
    <div className="space-y-8">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Your labeled items</h1>
          <p className="text-sm text-slate-500">Search, manage and print labels with ease.</p>
        </div>
        <Link
          href="/new"
          className="rounded-full bg-brand-500 px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-600"
        >
          New item
        </Link>
      </header>

      <form className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
        <input
          type="search"
          name="q"
          defaultValue={searchParams?.q ?? ""}
          placeholder="Search by title or tag"
          className="flex-1 rounded-md border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
        />
        <button type="submit" className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
          Search
        </button>
      </form>

      {items.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">
          No items yet. Create your first label!
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => (
            <ItemCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
}
