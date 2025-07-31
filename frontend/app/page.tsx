"use client";

import { useEffect, useState } from "react";
import { login } from "@/lib/api";
import GenreSummaryTable from "./components/GenreSummaryTable";
import UnsoldGenreTable from "./components/UnsoldGenresTable";

type GenreSummary = {
  genre: string;
  "sales-count": number;
  "last-sale-date": string;
  "last-track-sold": string;
};

type NotSoldGenre = {
  GenreId: number;
  Name: string;
};

export default function Home() {
  const [totalGenres, setTotalGenres] = useState<number>(0);
  const [recentSale, setRecentSale] = useState<{ genre: string; "date-sold": string } | null>(null);
  const [genreSummaries, setGenreSummaries] = useState<GenreSummary[]>([]);
  const [notSoldGenres, setNotSoldGenres] = useState<NotSoldGenre[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1) Log in and get token
        const token = await login("nancy@chinookcorp.com", "password123");

        // 2) Fetch all endpoints
        const [totalRes, recentRes, summaryRes, notSoldRes] = await Promise.all([
          fetch("http://localhost:8000/total-genre"),
          fetch("http://localhost:8000/recent-sale"),
          fetch("http://localhost:8000/genre-sale-summary", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch("http://localhost:8000/not-sold"),
        ]);

        if (!totalRes.ok) throw new Error("Failed to load total-genre");
        if (!recentRes.ok) throw new Error("Failed to load recent-sale");
        if (!summaryRes.ok) throw new Error("Failed to load genre-summary");
        if (!notSoldRes.ok) throw new Error("Failed to load not-sold");

        // 3) Parse JSON
        const totalData = await totalRes.json();
        const recentData = await recentRes.json();
        const summaryData = await summaryRes.json();
        const notSoldData = await notSoldRes.json();

        // 4) Set state
        setTotalGenres(totalData["total-genre-sold"]);
        setRecentSale(recentData);
        setGenreSummaries(summaryData);
        setNotSoldGenres(notSoldData);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return isNaN(date.getTime()) ? "Invalid Date" : date.toLocaleDateString();
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Distribution of sales by genre</h2>

      <section className="mt-8">
        <p><strong>Number of music genres sold</strong>: {totalGenres}</p>
      </section>

      <section className="mb-8">
        <p>
          <strong>Most recent Sale</strong>:{" "}
          {recentSale
            ? `${recentSale.genre} on ${formatDate(recentSale["date-sold"])}`
            : "—"}
        </p>
      </section>

      <section>
        <h3>Genre Sale Summary</h3>
        <GenreSummaryTable data={genreSummaries} formatDate={formatDate} />
      </section>

      <section className="mt-8">
        <h3>Genres Not Sold</h3>
        <UnsoldGenreTable data={notSoldGenres} />
      </section>
    </div>
  );
}