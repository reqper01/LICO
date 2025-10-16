export interface ItemImage {
  id: string;
  path: string;
  created_at: string;
}

export interface Item {
  id: string;
  short_id: string;
  title: string;
  description: string;
  tags: string[];
  location?: string | null;
  status: string;
  images: ItemImage[];
  created_at: string;
  updated_at: string;
}

export interface ItemSuggestions {
  title: string;
  description: string;
  tags: string[];
}
