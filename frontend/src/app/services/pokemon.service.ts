import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PokemonService {

  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getPokemons(offset: number): Observable<Pokemon[]> {
    return this.http.get<Pokemon[]>(`${this.baseUrl}/pokemon?offset=${offset}&limit=20`);
  }

  getPokemonInfo(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/pokemon/${id}`)
  }

  searchPokemons(term: string): Observable<Pokemon[]>{
    return this.http.get<Pokemon[]>(`${this.baseUrl}/pokemon?search=${term}`)
  }
}


export interface Pokemon {
  id: number;
  name: string;
}