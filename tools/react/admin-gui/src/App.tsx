import { useState } from "react";
import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
  DataProvider,
} from "react-admin";

import Login from "./Login";
import { IndicationCreate } from "./Indication";
import { HerbaTealList, HerbalTeaEdit, HerbalTeaShow } from "./HerbalTea";

function App() {
  const [user, setUser] = useState(null);
  const [dataProvider, setDataProvider] = useState<DataProvider | null>(null);

  return (
    <div className="App">
      {dataProvider ? (
        <Admin dataProvider={dataProvider}>
          <Resource
            name="herbaltea"
            list={HerbaTealList}
            edit={HerbalTeaEdit}
            show={HerbalTeaShow}
          />
          <Resource
            name="indication"
            list={ListGuesser}
            edit={EditGuesser}
            show={ShowGuesser}
            create={IndicationCreate}
            recordRepresentation="name"
          />
        </Admin>
      ) : (
        <Login
          user={user}
          setUser={setUser}
          setDataProvider={setDataProvider}
        />
      )}
    </div>
  );
}

export default App;
