import { useContext } from "react";
import {
  Grid,
  Typography,
  Card,
  CardContent,
  Box,
  CardActions,
} from "@mui/material";

import { HerbalTeaGet } from "./Types";
import IndicationChip from "./IndicationChip";
import LinkButton from "./LinkButton";
import { IndicationListContext } from "./IndicationListContext";

interface HerbalTeaItemProps {
  herbalTea: HerbalTeaGet;
}

export default function HerbalTeaCard({ herbalTea }: HerbalTeaItemProps) {
  const indicationData = useContext(IndicationListContext).object;
  return (
    <Grid item key={herbalTea.id} xs={12} sm={12} md={6} lg={4}>
      <Card sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {herbalTea.name_fr}
          </Typography>
          <Box>
            <Typography variant="body2" color="text.secondary">
              {herbalTea.name_botanical}
            </Typography>
            {indicationData && herbalTea.indication_ids
              ? herbalTea.indication_ids.map((indicationId: number) => (
                  <IndicationChip
                    key={indicationId}
                    label={indicationData[indicationId].name}
                  />
                ))
              : null}
          </Box>
        </CardContent>
        <CardActions sx={{ mt: "auto" }}>
          {herbalTea.monograph_url ? (
            <LinkButton label="Monograph" url={herbalTea.monograph_url} />
          ) : null}
          {herbalTea.gbif_id ? (
            <LinkButton
              label="GBIF"
              url={"https://www.gbif.org/fr/species/" + herbalTea.gbif_id}
            />
          ) : null}
        </CardActions>
      </Card>
    </Grid>
  );
}
