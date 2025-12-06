"use client";

import { useState, useEffect } from "react";

interface DnDItem {
  name: string;
  index: string;
  level?: number;
  [key: string]: any;
}

interface DnDData {
  results: DnDItem[];
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<
    "races" | "classes" | "spells" | "monsters"
  >("races");
  const [data, setData] = useState<Record<string, DnDItem[]>>({});
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<DnDItem | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const tabs: Array<"races" | "classes" | "spells" | "monsters"> = [
        "races",
        "classes",
        "spells",
        "monsters",
      ];
      const loadedData: Record<string, DnDItem[]> = {};

      for (const tab of tabs) {
        try {
          const response = await fetch(`/api/dnd?category=${tab}`);
          if (response.ok) {
            const json: DnDData = await response.json();
            loadedData[tab] = json.results || [];
          }
        } catch (e) {
          console.error(`Failed to load ${tab}:`, e);
          loadedData[tab] = [];
        }
      }

      setData(loadedData);
      setLoading(false);
    } catch (error) {
      console.error("Error loading data:", error);
      setLoading(false);
    }
  };

  const handleItemClick = async (item: DnDItem, tab: string) => {
    try {
      const response = await fetch(
        `/api/dnd?category=${tab}&index=${item.index}`
      );
      if (response.ok) {
        const details: DnDItem = await response.json();
        setSelectedItem({ ...details, type: tab });
      } else {
        setSelectedItem({ ...item, type: tab });
      }
    } catch (e) {
      setSelectedItem({ ...item, type: tab });
    }
  };

  const speakText = async (text: string) => {
    try {
      const response = await fetch("/api/tts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text.toUpperCase() + "!" }),
      });

      if (response.ok) {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("audio")) {
          const audioBlob = await response.blob();
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          audio.play();
        } else {
          const errorData = await response.json();
          console.error("TTS failed:", errorData);
          alert(
            `TTS Error: ${
              errorData.message || errorData.error || "Unknown error"
            }`
          );
        }
      } else {
        let errorMessage = response.statusText;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorData.error || errorMessage;
        } catch (e) {}
        console.error("TTS failed:", errorMessage);
        alert(`TTS Error: ${errorMessage}`);
      }
    } catch (e) {
      console.error("Error with TTS:", e);
      alert(`TTS Error: ${e instanceof Error ? e.message : "Network error"}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Loading D&D data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <h1 className="text-3xl font-bold">D&D 5e Data Viewer</h1>
      </header>
      <div className="flex">
        <aside className="w-64 bg-gray-800 border-r border-gray-700 p-4">
          <nav className="space-y-2">
            {(["races", "classes", "spells", "monsters"] as const).map(
              (tab) => (
                <button
                  key={tab}
                  onClick={() => {
                    setActiveTab(tab);
                    setSelectedItem(null);
                  }}
                  className={`w-full text-left px-4 py-2 rounded ${
                    activeTab === tab
                      ? "bg-blue-600 text-white"
                      : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              )
            )}
          </nav>
        </aside>
        <main className="flex-1 p-6">
          {selectedItem ? (
            <div>
              <div className="flex gap-2 mb-4">
                <button
                  onClick={() => setSelectedItem(null)}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
                >
                  ← Back
                </button>
                <button
                  onClick={() =>
                    speakText(selectedItem.name || selectedItem.index)
                  }
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded font-semibold"
                >
                  🔊 Speak
                </button>
              </div>
              <ItemDetails item={selectedItem} />
            </div>
          ) : (
            <ItemList
              items={data[activeTab] || []}
              tab={activeTab}
              onItemClick={handleItemClick}
              onSpeak={speakText}
            />
          )}
        </main>
      </div>
    </div>
  );
}

function ItemList({
  items,
  tab,
  onItemClick,
  onSpeak,
}: {
  items: DnDItem[];
  tab: string;
  onItemClick: (item: DnDItem, tab: string) => void;
  onSpeak: (text: string) => void;
}) {
  if (!items || items.length === 0) {
    return <div className="text-gray-400">No {tab} data available.</div>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4 capitalize">
        {tab} ({items.length})
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="bg-gray-800 p-4 rounded-lg border border-gray-700"
          >
            <div
              onClick={() => onItemClick(item, tab)}
              className="cursor-pointer hover:bg-gray-700 rounded p-2 -m-2"
            >
              <h3 className="font-semibold text-lg">{item.name}</h3>
              {item.level !== undefined && (
                <p className="text-gray-400 text-sm">Level {item.level}</p>
              )}
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onSpeak(item.name);
              }}
              className="mt-2 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-semibold"
            >
              🔊 Speak
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function ItemDetails({ item }: { item: DnDItem }) {
  const renderValue = (value: any) => {
    if (value === null || value === undefined) return null;
    if (typeof value === "object") {
      if (Array.isArray(value)) {
        return (
          <ul className="list-disc list-inside ml-4">
            {value.map((v, i) => (
              <li key={i}>
                {typeof v === "object" ? JSON.stringify(v) : String(v)}
              </li>
            ))}
          </ul>
        );
      }
      return (
        <pre className="bg-gray-800 p-2 rounded text-sm overflow-x-auto">
          {JSON.stringify(value, null, 2)}
        </pre>
      );
    }
    return <span>{String(value)}</span>;
  };

  const entries = Object.entries(item).filter(
    ([key]) => key !== "name" && key !== "index" && key !== "type"
  );

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <h2 className="text-3xl font-bold mb-4">{item.name || item.index}</h2>
      <div className="space-y-4">
        {entries.map(([key, value]) => (
          <div key={key}>
            <h3 className="font-semibold text-lg capitalize mb-1">
              {key.replace(/_/g, " ")}
            </h3>
            <div className="text-gray-300 ml-4">{renderValue(value)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
