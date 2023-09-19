import { useState } from "react";
import { Grid, Stack, Pagination } from "@mui/material";
import { useQuery } from "react-query";

import HerbalTeaCard from "./HerbalTeaCard";
import { HerbalTeaGet } from "./Types";
import { data_api_url } from "./Urls";
import IndicationFilter from "./IndicationFilter";

const limit = 12;

export default function HerbalTeaList() {
  const [page, setPage] = useState(1);
  const [pageCount, setPageCount] = useState(0);
  const [indicationSelected, setindicationSelected] = useState([]);

  const handleChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const offset = (page - 1) * limit;

  const indicationFilter = indicationSelected
    ? `&indication_ids=cs.{${indicationSelected}}`
    : "";

  const herbalTeaEndpoint = `${data_api_url}/herbaltea?limit=${limit}&offset=${offset}&order=name_fr${indicationFilter}`;

  const getHerbalTeas = async (page: number): Promise<HerbalTeaGet[]> => {
    const res = await fetch(herbalTeaEndpoint, {
      headers: { Prefer: "count=exact" },
    });

    if (!res.ok) {
      return [];
    }

    const contentRange = res.headers.get("content-range") || "/0";
    setPageCount(Math.ceil(parseInt(contentRange.split("/")[1]) / limit));
    return res.json();
  };

  const { isLoading, error, data } = useQuery({
    queryKey: [herbalTeaEndpoint, page],
    queryFn: async () => {
      return await getHerbalTeas(page);
    },
    keepPreviousData: true,
  });

  if (isLoading) return <div>Loading...</div>;

  if (error) return <div>{"An error has occurred: "}</div>; // + error.message

  const listItems = data
    ? data.map((item: HerbalTeaGet) => (
        <HerbalTeaCard key={item.id} herbalTea={item} />
      ))
    : [];

  return (
    <Stack alignItems="center" spacing={2}>
      <IndicationFilter
        indicationSelected={indicationSelected}
        setindicationSelected={setindicationSelected}
        setPage={setPage}
      />
      <Grid container spacing={4}>
        {listItems}
      </Grid>
      <Pagination count={pageCount} onChange={handleChange} page={page} />
    </Stack>
  );
}
