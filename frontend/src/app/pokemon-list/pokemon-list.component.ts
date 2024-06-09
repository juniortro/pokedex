import { Component, ElementRef } from '@angular/core';
import { PokemonService, Pokemon } from '../services/pokemon.service';
import { Subject, Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { PokemonDialogComponent } from '../pokemon-dialog/pokemon-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-pokemon-list',
  templateUrl: './pokemon-list.component.html',
  styleUrls: ['./pokemon-list.component.css']
})
export class PokemonListComponent {
  pokemons: Pokemon[] = [];
  pokemonDetails: any[] = [];
  searchedPokemons: Pokemon[] = [];
  private searchTerms = new Subject<string>();
  currentPage: number = 0

  constructor(private pokemonService: PokemonService, private dialog: MatDialog){}

  ngOnInit(){
    this.getPokemons();
    this.searchPokemons();
  }

  getPokemons(){
    this.pokemonService.getPokemons(this.currentPage)
      .subscribe(data => {
        this.pokemons = data;
        this.getPokemonDetails();
      });
  }

  getPokemonDetails(){
    for(let pokemon of this.pokemons){
      this.pokemonService.getPokemonInfo(pokemon.id)
        .subscribe(data => {
          this.pokemonDetails[pokemon.id] = data;
        });
    }
  }

  getPokemonImageUrl(pokemonId: number){
    return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pokemonId}.png`;
  }

  search(input: HTMLInputElement): void {
    const term = input.value;
    this.searchTerms.next(term);
  }

  private searchPokemons(): void {
    this.searchTerms.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap((term: string) => this.searchPokemon(term))
    ).subscribe((pokemons: Pokemon[]) => {
      this.pokemons = pokemons
    });
  }

  private searchPokemon(term: string): Observable<Pokemon[]> {
    if (!term.trim()) {
      this.getPokemons()
      return of([]);
    }
    return this.pokemonService.searchPokemons(term);
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage = this.currentPage - 20;
      this.getPokemons();
    }
  }

  nextPage(): void {
    this.currentPage = this.currentPage + 20;
    this.getPokemons();
  }

  openPokemonDialog(pokemon: Pokemon): void {
    const pokemonDetail = this.pokemonDetails[pokemon.id];
    const dialogRef = this.dialog.open(PokemonDialogComponent, {
      width: '250px',
      data: { pokemon, pokemonDetail }
    });
  }
}
