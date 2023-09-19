export interface HerbalTeaGet {
  name_botanical: string;
  name_fr?: string;
  monograph_url?: string;
  indication_raw?: string;
  indication_ids?: number[];
  gbif_id?: number;
  id: number;
}

export interface IndicationGet {
  name: string;
  description?: string;
  id: number;
}
