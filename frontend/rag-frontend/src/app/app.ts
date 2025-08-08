import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { QueryFormComponent } from './query-form/query-form'; // path corretto

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, QueryFormComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  protected readonly title = signal('rag-frontend');
}
