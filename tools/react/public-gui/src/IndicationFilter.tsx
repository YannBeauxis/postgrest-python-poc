import { useContext } from "react";
import { ButtonGroup, Button, useMediaQuery } from "@mui/material";
import { useTheme } from "@mui/material/styles";

import { IndicationListContext } from "./IndicationListContext";
import { IndicationGet } from "./Types";

interface IndicationFilterProps {
  indicationSelected: number[];
  setindicationSelected: any;
  setPage: any;
}

export default function IndicationFilter({
  indicationSelected,
  setindicationSelected,
  setPage,
}: IndicationFilterProps) {
  const indicationList = useContext(IndicationListContext).array;

  const toggleSelect = (indicationId: number) => {
    const newSelection = [...indicationSelected];
    const index = newSelection.indexOf(indicationId);
    index > -1
      ? newSelection.splice(index, 1)
      : newSelection.push(indicationId);
    setPage(1);
    setindicationSelected(newSelection);
  };

  const theme = useTheme();
  const matches = useMediaQuery(theme.breakpoints.up("sm"));

  return (
    <ButtonGroup
      variant="outlined"
      orientation={`${matches ? `horizontal` : `vertical`}`}
    >
      {indicationList
        ? indicationList.map((indication: IndicationGet) => (
            <Button
              key={indication.id}
              onClick={() => {
                toggleSelect(indication.id);
              }}
              variant={
                indicationSelected.includes(indication.id)
                  ? "contained"
                  : "outlined"
              }
            >
              {indication.name}
            </Button>
          ))
        : null}
    </ButtonGroup>
  );
}
