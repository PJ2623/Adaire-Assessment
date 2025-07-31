type NotSoldGenre = {
  GenreId: number;
  Name: string;
};

type Props = {
  data: NotSoldGenre[];
};

export default function UnsoldGenreTable({ data }: Props) {
  return (
    <table className="table-auto border border-collapse">
      <thead>
        <tr className="bg-gray-100">
          <th className="border px-4 py-2 text-left">#</th>
          <th className="border px-4 py-2 text-left">Music Genre</th>
        </tr>
      </thead>
      <tbody>
        {data.map((genre, index) => (
          <tr key={genre.GenreId} className="even:bg-gray-50">
            <td className="border px-4 py-2">{index + 1}</td>
            <td className="border px-4 py-2">{genre.Name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}