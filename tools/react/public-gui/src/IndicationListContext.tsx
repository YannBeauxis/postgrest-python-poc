import { createContext, useMemo } from "react";
import { useQuery } from "react-query";

import { data_api_url } from "./Urls";
import { IndicationGet } from "./Types";

interface IndicationListContextType {
  array: IndicationGet[];
  object: { [key: string]: IndicationGet };
}

export const IndicationListContext = createContext<IndicationListContextType>({
  array: [],
  object: {},
});

interface IndicationListContextProviderProps {
  children: any;
}

export function IndicationListProvider({
  children,
}: IndicationListContextProviderProps) {
  const indicationEndpoint = `${data_api_url}/indication`;

  const indicationQuery = useQuery({
    queryKey: ["/indication"],
    queryFn: async () => {
      const res = await fetch(indicationEndpoint);
      if (res.ok) {
        return res.json();
      } else {
        return [];
      }
    },
    keepPreviousData: true,
  });

  const indicationArray = indicationQuery.data;

  const indicationObject = useMemo(
    () =>
      indicationQuery.data
        ? indicationQuery.data.reduce(
            (indications: any, indication: IndicationGet) => {
              indications[indication.id] = indication;
              return indications;
            },
            {}
          )
        : {},
    [indicationQuery.data]
  );

  return (
    <IndicationListContext.Provider
      value={{ object: indicationObject, array: indicationArray }}
    >
      {children}
    </IndicationListContext.Provider>
  );
}
