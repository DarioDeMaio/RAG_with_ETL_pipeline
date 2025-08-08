import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';  // <-- importa NgIf

@Component({
  selector: 'app-query-form',
  standalone: true,
  imports: [HttpClientModule, FormsModule, NgIf],
  templateUrl: './query-form.html',
  styleUrls: ['./query-form.css']
})
export class QueryFormComponent {
  domanda = '';
  risposta: { answer: string } | null = null;

  constructor(private http: HttpClient) {}

  inviaDomanda() {
    this.http.post<{ answer: string }>('http://localhost:8000/query', { question: this.domanda })
      .subscribe({
        next: (data) => this.risposta = data,
        error: () => this.risposta = { answer: 'Errore nella risposta dal server.' }
      });
  }
}

