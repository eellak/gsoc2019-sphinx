import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule, ExtraOptions } from '@angular/router';
import { LanguageAdaptationComponent } from '../language-adaptation/language-adaptation.component';
import { AcousticAdaptationComponent } from '../acoustic-adaptation/acoustic-adaptation.component';
import { DictationComponent } from '../dictation/dictation.component';
import { LogInComponent } from '../log-in/log-in.component';

const routes: Routes = [
  { path: 'log-in', component: LogInComponent },
  { path: '', redirectTo: '/log-in', pathMatch: 'full' },
  { path: 'acoustic', component: AcousticAdaptationComponent },
  { path: 'language', component: LanguageAdaptationComponent },
  { path: 'dictation', component: DictationComponent }
];

@NgModule({
  declarations: [
  ],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class RoutingModule { }
