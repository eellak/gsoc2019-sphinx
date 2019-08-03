import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AcousticAdaptationComponent } from './acoustic-adaptation.component';

describe('AcousticAdaptationComponent', () => {
  let component: AcousticAdaptationComponent;
  let fixture: ComponentFixture<AcousticAdaptationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AcousticAdaptationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AcousticAdaptationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
