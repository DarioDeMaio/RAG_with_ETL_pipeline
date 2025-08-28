import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ChatMessage {
  type: 'user' | 'bot';
  content: string;
}

@Component({
  selector: 'app-rag-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './rag-chat.html',
  styleUrls: ['./rag-chat.css'],
})
export class RagChatComponent {
  messages: ChatMessage[] = [];
  userInput: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  sendMessage() {
    const question = this.userInput.trim();
    if (!question) return;

    this.messages.push({ type: 'user', content: question });
    this.userInput = '';
    this.loading = true;

    this.http.post<any>('http://localhost:8000/query', { question }).subscribe({
      next: (res) => {
        const answer = res.answer ?? 'Nessuna risposta generata';
        this.messages.push({ type: 'bot', content: answer });

        if (res.retrieved_documents?.length) {
          res.retrieved_documents.forEach((doc: string, i: number) => {
            this.messages.push({ type: 'bot', content: `  Doc ${i + 1}: ${doc}` });
          });
        }

        this.loading = false;

        setTimeout(() => {
          const container = document.querySelector('.messages');
          if (container) container.scrollTop = container.scrollHeight;
        }, 0);
      },
      error: (err) => {
        this.messages.push({ type: 'bot', content: "  Errore: " + err.message });
        this.loading = false;
      }
    });
  }
}

