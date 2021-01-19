import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalysisPageComponent } from './analysis-page.component';

describe('AnalysisPageComponent', () => {
  let component: AnalysisPageComponent;
  let fixture: ComponentFixture<AnalysisPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AnalysisPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AnalysisPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
