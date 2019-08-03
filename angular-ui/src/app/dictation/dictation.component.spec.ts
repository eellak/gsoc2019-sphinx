import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DictationComponent } from './dictation.component';

describe('DictationComponent', () => {
  let component: DictationComponent;
  let fixture: ComponentFixture<DictationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DictationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DictationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
