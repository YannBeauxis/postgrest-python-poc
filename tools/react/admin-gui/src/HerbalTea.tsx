import TextareaAutosize from "@mui/base/TextareaAutosize";
import { Box } from "@mui/system";
import { Typography, Card } from "@mui/material";
import {
  Show,
  Edit,
  SimpleForm,
  TextInput,
  TextField,
  SimpleShowLayout,
  List,
  UrlField,
  Datagrid,
  ReferenceArrayInput,
  ReferenceArrayField,
  useRecordContext,
  SelectArrayInput,
} from "react-admin";

const herbalTeaFilters = [
  <ReferenceArrayInput
    label="Indication"
    reference="indication"
    source="indication_ids@cs"
    alwaysOn
  >
    <SelectArrayInput label="Indication" />
  </ReferenceArrayInput>,
];

const IndicationRowField = ({ source }: { source: string }) => {
  const record = useRecordContext();
  return (
    <TextareaAutosize
      minRows={10}
      style={{ width: 900 }}
      value={record[source]}
      readOnly
    />
  );
};

export const HerbaTealList = () => (
  <List filters={herbalTeaFilters}>
    <Datagrid rowClick="edit">
      <TextField source="name_botanical" />
      <TextField source="name_fr" />
      <ReferenceArrayField reference="indication" source="indication_ids" />
    </Datagrid>
  </List>
);

export const HerbalTeaShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="name_botanical" />
      <ReferenceArrayField reference="indication" source="indication_ids" />
      <TextField source="name_fr" />
      <UrlField source="monograph_url" target="_blank" />
      <IndicationRowField source="indication_raw" />
    </SimpleShowLayout>
  </Show>
);

const Aside = () => (
  <Card sx={{ marginX: "1em" }}>
    <SimpleShowLayout>
      <Typography variant="h6">EMA monograph source</Typography>

      <IndicationRowField source="indication_raw" />
      <UrlField source="monograph_url" target="_blank" />
    </SimpleShowLayout>
  </Card>
);

export const HerbalTeaEdit = () => (
  <Edit aside={<Aside />}>
    <SimpleForm>
      <TextInput source="name_botanical" />
      <TextInput source="name_fr" />
      <ReferenceArrayInput reference="indication" source="indication_ids" />
    </SimpleForm>
  </Edit>
);
