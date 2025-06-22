/**
 * SKATECROSS QR - Wspólne typy API
 * Wersja: 2.0.0
 * Ujednolicone typy TypeScript dla wszystkich odpowiedzi API
 */

// === PODSTAWOWE TYPY API ===

/**
 * Standardowa struktura odpowiedzi API
 */
export interface APIResponse<T = any> {
  success: boolean;
  data: T | null;
  meta: APIMetadata;
  error: APIError | null;
  message?: string;
}

/**
 * Metadane odpowiedzi API
 */
export interface APIMetadata {
  timestamp: string;
  count: number | null;
  total: number | null;
  page: number | null;
  limit: number | null;
  [key: string]: any; // Dodatkowe metadane specyficzne dla endpointu
}

/**
 * Struktura błędu API
 */
export interface APIError {
  message: string;
  code: string | null;
  details: any | null;
}

/**
 * Parametry paginacji
 */
export interface PaginationParams {
  page?: number;
  limit?: number;
}

/**
 * Parametry filtrowania
 */
export interface FilterParams {
  season?: number;
  kategoria?: string;
  plec?: 'M' | 'K';
  klub?: string;
  [key: string]: any;
}

// === TYPY DANYCH DOMENOWYCH ===

/**
 * Zawodnik
 */
export interface Zawodnik {
  id?: number;
  nr_startowy: number;
  imie: string;
  nazwisko: string;
  kategoria: string;
  plec: 'M' | 'K';
  klub: string;
  qr_code?: string;
  czas_przejazdu_s?: number | null;
  status?: string;
  checked_in?: boolean;
}

/**
 * Wynik zawodnika
 */
export interface Wynik {
  nr_startowy: number;
  czas_przejazdu_s: number | null;
  status: 'FINISHED' | 'DNF' | 'DSQ' | 'PENDING';
  imie: string;
  nazwisko: string;
  kategoria: string;
  plec: 'M' | 'K';
}

/**
 * Ranking indywidualny
 */
export interface RankingIndywidualny {
  nr_startowy: number;
  imie: string;
  nazwisko: string;
  kategoria: string;
  plec: 'M' | 'K';
  klub: string;
  punkty: number;
  liczba_zawodow: number;
  najlepszy_czas: number | null;
}

/**
 * Ranking klubowy
 */
export interface RankingKlubowy {
  klub: string;
  punkty_total?: number;
  punkty_top3?: number;
  aktywne_kategorie: number;
  balance: number;
}

/**
 * Ranking medalowy
 */
export interface RankingMedalowy {
  klub: string;
  zlote: number;
  srebrne: number;
  brazowe: number;
  lacznie: number;
}

/**
 * Statystyki zawodników
 */
export interface StatystykiZawodnikow {
  kategorie: Record<string, { M: number; K: number }>;
  total: { M: number; K: number; razem: number };
}

/**
 * Lista kategorii
 */
export interface ListaKategorii {
  kategorie: string[];
  total_zawodnikow: number;
}

/**
 * Lista klubów
 */
export interface ListaKlubow {
  nazwy_klubow: string[];
  total_klubow: number;
}

/**
 * Element drabinki
 */
export interface ElementDrabinki {
  nr_startowy: number;
  imie: string;
  nazwisko: string;
  czas_przejazdu_s: number | null;
  pozycja?: number;
}

/**
 * Grupa w drabince
 */
export interface GrupaDrabinki {
  zawodnicy: ElementDrabinki[];
  typ: 'ćwierćfinał' | 'półfinał' | 'finał';
  numer_grupy: number;
}

/**
 * Drabinka kategoria
 */
export interface DrabinkaKategoria {
  statystyki: {
    łącznie_zawodników: number;
    z_czasami: number;
    w_ćwierćfinałach: number;
    grup_ćwierćfinały: number;
    grup_półfinały: number;
    grup_finał: number;
  };
  ćwierćfinały: GrupaDrabinki[];
  półfinały: GrupaDrabinki[];
  finał: GrupaDrabinki[];
}

/**
 * Pełna drabinka
 */
export interface DrabinkaTurniejowa {
  podsumowanie: {
    wszystkie_kategorie: string[];
    łączna_liczba_zawodników: number;
    w_ćwierćfinałach: number;
    podział_płeć: {
      mężczyźni: number;
      kobiety: number;
    };
  };
  [kategoria_plec: string]: DrabinkaKategoria | any;
}

/**
 * Podsumowanie rankingów
 */
export interface PodsumowanieRankingów {
  season: number | string;
  stats: {
    zawodnicy_total: number;
    zawodnicy_general: number;
    kluby_total: number;
    kluby_top3: number;
    kluby_z_medalami: number;
  };
  top_zawodnik: RankingIndywidualny | null;
  top_general: RankingIndywidualny | null;
  top_klub_total: RankingKlubowy | null;
  top_klub_top3: RankingKlubowy | null;
  top_medals: RankingMedalowy | null;
}

// === TYPY ODPOWIEDZI SPECYFICZNYCH ENDPOINTÓW ===

export type ZawodnicyResponse = APIResponse<Zawodnik[]>;
export type ZawodnikResponse = APIResponse<Zawodnik>;
export type WynikiResponse = APIResponse<Wynik[]>;
export type RankingIndywidualnyResponse = APIResponse<RankingIndywidualny[]>;
export type RankingKlubowyResponse = APIResponse<RankingKlubowy[]>;
export type RankingMedalowyResponse = APIResponse<RankingMedalowy[]>;
export type StatystykiResponse = APIResponse<StatystykiZawodnikow>;
export type KategorieResponse = APIResponse<ListaKategorii>;
export type KlubyResponse = APIResponse<ListaKlubow>;
export type DrabinkaResponse = APIResponse<DrabinkaTurniejowa>;
export type PodsumowanieResponse = APIResponse<PodsumowanieRankingów>;

// === KODY BŁĘDÓW ===

export enum ErrorCodes {
  VALIDATION_ERROR = "VALIDATION_ERROR",
  NOT_FOUND = "NOT_FOUND",
  UNAUTHORIZED = "UNAUTHORIZED",
  FORBIDDEN = "FORBIDDEN",
  CONFLICT = "CONFLICT",
  INTERNAL_ERROR = "INTERNAL_ERROR",
  BAD_REQUEST = "BAD_REQUEST",
  
  // Błędy specyficzne dla SKATECROSS
  ZAWODNIK_NOT_FOUND = "ZAWODNIK_NOT_FOUND",
  INVALID_QR_CODE = "INVALID_QR_CODE",
  RACE_TIME_INVALID = "RACE_TIME_INVALID",
  TOURNAMENT_PHASE_ERROR = "TOURNAMENT_PHASE_ERROR"
}

// === POMOCNICZE TYPY ===

/**
 * Status odpowiedzi HTTP
 */
export type HttpStatus = 200 | 201 | 400 | 401 | 403 | 404 | 409 | 500;

/**
 * Metody HTTP
 */
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * Konfiguracja zapytania API
 */
export interface APIRequestConfig {
  method: HttpMethod;
  url: string;
  params?: Record<string, any>;
  data?: any;
  headers?: Record<string, string>;
}

/**
 * Guard sprawdzający czy odpowiedź to sukces
 */
export function isSuccessResponse<T>(response: APIResponse<T>): response is APIResponse<T> & { success: true; data: T } {
  return response.success === true && response.data !== null;
}

/**
 * Guard sprawdzający czy odpowiedź to błąd
 */
export function isErrorResponse<T>(response: APIResponse<T>): response is APIResponse<T> & { success: false; error: APIError } {
  return response.success === false && response.error !== null;
}

/**
 * Typ pomocniczy dla extrakcji danych z odpowiedzi
 */
export type ExtractAPIData<T> = T extends APIResponse<infer U> ? U : never;

// === PRZYKŁADY UŻYCIA ===

// Przykład 1: Typowanie axios response
// const response: AxiosResponse<ZawodnicyResponse> = await axios.get('/api/zawodnicy');
// if (isSuccessResponse(response.data)) {
//   const zawodnicy: Zawodnik[] = response.data.data;
//   console.log(`Pobrano ${response.data.meta.count} zawodników`);
// }

// Przykład 2: Obsługa błędów
// if (isErrorResponse(response.data)) {
//   console.error(`Błąd ${response.data.error.code}: ${response.data.error.message}`);
// }

// Przykład 3: Paginacja
// const params: PaginationParams & FilterParams = {
//   page: 1,
//   limit: 50,
//   kategoria: 'Junior A',
//   plec: 'M'
// }; 