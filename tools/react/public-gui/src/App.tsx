import { Container, Box, Link, Typography } from "@mui/material";
import { QueryClient, QueryClientProvider } from "react-query";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { teal, blueGrey } from "@mui/material/colors";

import HerbalTeaList from "./HerbalTeaList";
import { IndicationListProvider } from "./IndicationListContext";

const theme = createTheme({
  palette: {
    primary: teal,
    secondary: blueGrey,
  },
});

const queryClient = new QueryClient();

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <QueryClientProvider client={queryClient}>
        <IndicationListProvider>
          <Container maxWidth="lg">
            <Box
              sx={{
                pt: 8,
                pb: 6,
              }}
            >
              <Typography variant="h4" component="h1" gutterBottom>
                EMA Herbal Teas
              </Typography>

              <HerbalTeaList />
            </Box>

            <Copyright />
          </Container>
        </IndicationListProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://pro.yannbeauxis.net/">
        Yann Beauxis
      </Link>{" "}
      {new Date().getFullYear()}.
    </Typography>
  );
}
