/**
 * SKATECROSS QR - API Client
 * Wersja: 2.0.0
 * Scentralizowany klient API z obsługą ujednoliconych odpowiedzi
 */

import axios, { AxiosResponse, AxiosError } from 'axios';
import { ref, readonly, type Ref } from 'vue';
import { 
  APIResponse, 
  ZawodnicyResponse, 
  ZawodnikResponse,
  RankingIndywidualnyResponse,
  RankingKlubowyResponse,
  RankingMedalowyResponse,
  StatystykiResponse,
  KategorieResponse,
  KlubyResponse,
  DrabinkaResponse,
  PodsumowanieResponse,
  PaginationParams,
  FilterParams,
  isSuccessResponse,
  isErrorResponse,
  Zawodnik
} from '../types/api';

// === KONFIGURACJA API CLIENT ===

/**
 * Bazowa konfiguracja axios
 */
const apiClient = axios.create({
  timeout: 30000, // 30 sekund
  headers: {
    'Content-Type': 'application/json',
  }
});

/**
 * Interceptor dla requestów - dodaje logowanie
 */
apiClient.interceptors.request.use(
  (config) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] API Request: ${config.method?.toUpperCase()} ${config.url}`, config.params);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Interceptor dla odpowiedzi - obsługa błędów i logowanie
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse<APIResponse>) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] API Response: ${response.status}`, {
      url: response.config.url,
      success: response.data.success,
      count: response.data.meta.count,
      message: response.data.message
    });
    return response;
  },
  (error: AxiosError<APIResponse>) => {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] API Error:`, {
      url: error.config?.url,
      status: error.response?.status,
      message: error.response?.data?.error?.message || error.message
    });
    return Promise.reject(error);
  }
);

// === KLASA API CLIENT ===

export class SkatecrossAPI {
  
  // === ZAWODNICY ===
  
  /**
   * Pobiera listę zawodników z opcjonalną paginacją
   */
  static async getZawodnicy(params?: PaginationParams): Promise<ZawodnicyResponse> {
    const response = await apiClient.get<ZawodnicyResponse>('/api/zawodnicy', { params });
    return response.data;
  }

  /**
   * Pobiera pojedynczego zawodnika po numerze startowym
   */
  static async getZawodnik(nrStartowy: number): Promise<ZawodnikResponse> {
    const response = await apiClient.get<ZawodnikResponse>(`/api/zawodnicy/${nrStartowy}`);
    return response.data;
  }

  /**
   * Pobiera zawodników z określonej kategorii
   */
  static async getZawodnicyKategoria(
    kategoria: string, 
    filters?: FilterParams & PaginationParams
  ): Promise<ZawodnicyResponse> {
    const response = await apiClient.get<ZawodnicyResponse>(`/api/zawodnicy/kategoria/${kategoria}`, { 
      params: filters 
    });
    return response.data;
  }

  // === RANKINGI ===

  /**
   * Pobiera ranking indywidualny
   */
  static async getRankingIndywidualny(params?: FilterParams & PaginationParams): Promise<RankingIndywidualnyResponse> {
    const response = await apiClient.get<RankingIndywidualnyResponse>('/api/rankings/individual', { params });
    return response.data;
  }

  /**
   * Pobiera ranking generalny (n-2)
   */
  static async getRankingGeneralny(params?: FilterParams & PaginationParams): Promise<RankingIndywidualnyResponse> {
    const response = await apiClient.get<RankingIndywidualnyResponse>('/api/rankings/general', { params });
    return response.data;
  }

  /**
   * Pobiera ranking klubowy (wszyscy zawodnicy)
   */
  static async getRankingKlubowyTotal(params?: FilterParams & PaginationParams): Promise<RankingKlubowyResponse> {
    const response = await apiClient.get<RankingKlubowyResponse>('/api/rankings/clubs/total', { params });
    return response.data;
  }

  /**
   * Pobiera ranking klubowy (top 3)
   */
  static async getRankingKlubowyTop3(params?: FilterParams & PaginationParams): Promise<RankingKlubowyResponse> {
    const response = await apiClient.get<RankingKlubowyResponse>('/api/rankings/clubs/top3', { params });
    return response.data;
  }

  /**
   * Pobiera ranking medalowy
   */
  static async getRankingMedalowy(params?: FilterParams & PaginationParams): Promise<RankingMedalowyResponse> {
    const response = await apiClient.get<RankingMedalowyResponse>('/api/rankings/medals', { params });
    return response.data;
  }

  /**
   * Pobiera podsumowanie rankingów
   */
  static async getPodsumowanieRankingów(season?: number): Promise<PodsumowanieResponse> {
    const response = await apiClient.get<PodsumowanieResponse>('/api/rankings/summary', { 
      params: season ? { season } : undefined 
    });
    return response.data;
  }

  // === STATYSTYKI ===

  /**
   * Pobiera statystyki zawodników
   */
  static async getStatystyki(): Promise<StatystykiResponse> {
    const response = await apiClient.get<StatystykiResponse>('/api/statystyki');
    return response.data;
  }

  /**
   * Pobiera listę kategorii
   */
  static async getKategorie(): Promise<KategorieResponse> {
    const response = await apiClient.get<KategorieResponse>('/api/kategorie');
    return response.data;
  }

  /**
   * Pobiera listę klubów
   */
  static async getKluby(): Promise<KlubyResponse> {
    const response = await apiClient.get<KlubyResponse>('/api/kluby');
    return response.data;
  }

  // === DRABINKA ===

  /**
   * Pobiera drabinkę turniejową
   */
  static async getDrabinka(): Promise<DrabinkaResponse> {
    const response = await apiClient.get<DrabinkaResponse>('/api/drabinka');
    return response.data;
  }

  // === POMOCNICZE METODY ===

  /**
   * Bezpieczne wywołanie API z obsługą błędów
   */
  static async safeApiCall<T>(
    apiCall: () => Promise<APIResponse<T>>,
    defaultValue: T
  ): Promise<{ success: boolean; data: T; error?: string }> {
    try {
      const response = await apiCall();
      
      if (isSuccessResponse(response)) {
        return {
          success: true,
          data: response.data
        };
      } else if (isErrorResponse(response)) {
        return {
          success: false,
          data: defaultValue,
          error: response.error.message
        };
      } else {
        return {
          success: false,
          data: defaultValue,
          error: 'Nieoczekiwany format odpowiedzi'
        };
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Nieznany błąd';
      return {
        success: false,
        data: defaultValue,
        error: errorMessage
      };
    }
  }

  /**
   * Sprawdza dostępność API
   */
  static async healthCheck(): Promise<boolean> {
    try {
      const response = await apiClient.get('/api/version');
      return response.status === 200;
    } catch {
      return false;
    }
  }
}

// === COMPOSABLES (dla Vue 3) ===

/**
 * Composable do obsługi zawodników
 */
export function useZawodnicy() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const zawodnicy = ref<Zawodnik[]>([]);

  const fetchZawodnicy = async (params?: PaginationParams) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await SkatecrossAPI.getZawodnicy(params);
      
      if (isSuccessResponse(response)) {
        zawodnicy.value = response.data;
      } else if (isErrorResponse(response)) {
        error.value = response.error.message;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Błąd pobierania zawodników';
    } finally {
      loading.value = false;
    }
  };

  return {
    loading: readonly(loading),
    error: readonly(error),
    zawodnicy: readonly(zawodnicy),
    fetchZawodnicy
  };
}

/**
 * Composable do obsługi rankingów
 */
export function useRankingi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchRanking = async <T>(
    fetcher: () => Promise<APIResponse<T[]>>,
    target: Ref<T[]>
  ) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetcher();
      
      if (isSuccessResponse(response)) {
        target.value = response.data;
      } else if (isErrorResponse(response)) {
        error.value = response.error.message;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Błąd pobierania rankingu';
    } finally {
      loading.value = false;
    }
  };

  return {
    loading: readonly(loading),
    error: readonly(error),
    fetchRanking
  };
}

// === RE-EXPORTY ===

export { 
  isSuccessResponse, 
  isErrorResponse, 
  type APIResponse,
  type Zawodnik,
  type RankingIndywidualny,
  type RankingKlubowy,
  type RankingMedalowy
} from '../types/api';

// === DOMYŚLNY EXPORT ===

export default SkatecrossAPI; 