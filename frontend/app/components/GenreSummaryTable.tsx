type GenreSummary = {
  genre: string;
  "sales-count": number;
  "last-sale-date": string;
  "last-track-sold": string;
};

type Props = {
  data: GenreSummary[];
  formatDate: (dateStr: string) => string;
};

export default function GenreSummaryTable({ data, formatDate }: Props) {
  return (
    <table className="table-auto border border-collapse">
      <thead>
        <tr className="bg-gray-100">
          <th className="border px-4 py-2 text-left">#</th>
          <th className="border px-4 py-2 text-left">Music Genre</th>
          <th className="border px-4 py-2 text-left">Number of Sales</th>
          <th className="border px-4 py-2 text-left">Last Sale</th>
          <th className="border px-4 py-2 text-left">Last Track Sold</th>
        </tr>
      </thead>
      <tbody>
        {data.map((genre, index) => (
          <tr key={index} className="even:bg-gray-50">
            <td className="border px-4 py-2">{index + 1}</td>
            <td className="border px-4 py-2">{genre.genre}</td>
            <td className="border px-4 py-2">{genre["sales-count"]}</td>
            <td className="border px-4 py-2">{formatDate(genre["last-sale-date"])}</td>
            <td className="border px-4 py-2">{genre["last-track-sold"]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}