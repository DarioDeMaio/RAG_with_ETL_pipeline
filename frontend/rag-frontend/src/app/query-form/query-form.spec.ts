import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QueryForm } from './query-form';

describe('QueryForm', () => {
  let component: QueryForm;
  let fixture: ComponentFixture<QueryForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QueryForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QueryForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
