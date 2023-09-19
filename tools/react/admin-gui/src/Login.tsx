import {
  Button,
  TextField as MuiTextField,
  Stack,
  Container,
} from "@mui/material";
import { fetchUtils } from "react-admin";
import postgrestRestProvider from "@raphiniert/ra-data-postgrest";
import { Magic } from "magic-sdk";

const magic = new Magic("pk_live_4B21803FBEDD622A", { network: "mainnet" });
const auth_api_url =
  process.env.REACT_APP_AUTH_API_URL || "http://localhost:8000";
const data_api_url =
  process.env.REACT_APP_DATA_API_URL || "http://localhost:3001";
/* Connect to any email input or enter your own */
//  magic.auth.loginWithEmailOTP({ email: "dev@yannbeauxis.net" }).then(didToken => {
//    magic.user.getMetadata();//.then(userData => console.log(userData));
//       });

function Login({
  user,
  setUser,
  setDataProvider,
}: {
  user: any;
  setUser: any;
  setDataProvider: any;
}) {
  function handleLogin(e: any) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const email = formData.get("email");
    if (typeof email === "string") {
      magic.auth.loginWithMagicLink({ email }).then((didToken) => {
        fetch(auth_api_url + "/token", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ did_token: didToken }),
        })
          .then((response) => response.json())
          .then((data) => {
            const httpClient = (url: string, options: any = {}) => {
              options.user = {
                authenticated: true,
                token: "Bearer " + data.token,
              };
              return fetchUtils.fetchJson(url, options);
            };
            setDataProvider(postgrestRestProvider(data_api_url, httpClient));
          });
        //
        magic.user.getMetadata().then((userData) => setUser(userData));
      });
      // magic.user.isLoggedIn().then(isLoggedIn => {
      //   return isLoggedIn ? ) : setUser(null); return Promise.resolve(null);;
    }
    // magic.user.getIdToken().then(didToken => setDidToken(didToken));
  }

  // function handleLogout(e) {
  //   e.preventDefault();
  //   magic.user.logout().then(data => { setUser(null); setDidToken(null); });
  // }

  return (
    <Container>
      <h1>Enter your email to login</h1>
      <form onSubmit={handleLogin}>
        <Stack
          direction="row"
          justifyContent="flex-start"
          alignItems="center"
          spacing={2}
        >
          <MuiTextField label="email" name="email" required={true} />
          <Button type="submit" variant="contained">
            Login
          </Button>
        </Stack>
      </form>
    </Container>
  );
  // return <div style={{
  //   position: "absolute",
  //   top: "0",
  //   right: "10px",
  //   zIndex: 10
  // }}><p >Logged as {user.email} </p>
  //   <Button variant="contained" type="submit" onClick={handleLogout}>Logout</Button>
  // </div >
}
export default Login;
