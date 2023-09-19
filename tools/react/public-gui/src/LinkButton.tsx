import { Button } from "@mui/material";

interface LinkButtonProps {
  label: string;
  url: string;
}

export default function LinkButton({ label, url }: LinkButtonProps) {
  return (
    <Button
      size="small"
      variant="outlined"
      color="secondary"
      href={url}
      target="_blank"
    >
      {label}
    </Button>
  );
}
