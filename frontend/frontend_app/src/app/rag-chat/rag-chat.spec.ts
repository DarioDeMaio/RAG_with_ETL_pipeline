import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RagChat } from './rag-chat';

describe('RagChat', () => {
  let component: RagChat;
  let fixture: ComponentFixture<RagChat>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RagChat]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RagChat);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
