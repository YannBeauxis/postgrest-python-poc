/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface HerbalTeaCreate {
  name_botanical: string;
  name_fr?: string;
  monograph_url?: string;
  indication_raw?: string;
  indication_ids?: number[];
}
export interface HerbalTeaGet {
  name_botanical: string;
  name_fr?: string;
  monograph_url?: string;
  indication_raw?: string;
  indication_ids?: number[];
  id: number;
}
export interface IndicationCreate {
  name: string;
  description?: string;
}
export interface IndicationGet {
  name: string;
  description?: string;
  id: number;
}
