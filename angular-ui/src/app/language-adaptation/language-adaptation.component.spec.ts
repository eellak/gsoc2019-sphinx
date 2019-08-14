import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LanguageAdaptationComponent } from './language-adaptation.component';

describe('LanguageAdaptationComponent', () => {
  let component: LanguageAdaptationComponent;
  let fixture: ComponentFixture<LanguageAdaptationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [LanguageAdaptationComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LanguageAdaptationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
