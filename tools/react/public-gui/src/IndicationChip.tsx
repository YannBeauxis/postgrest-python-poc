import { Chip } from "@mui/material";

interface IndicationChipProps {
  label: string;
}

export default function IndicationChip({ label }: IndicationChipProps) {
  return <Chip size="small" label={label} sx={{ mr: 1 }} color="primary" />;
}
