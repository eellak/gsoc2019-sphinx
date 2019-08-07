import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule, ExtraOptions } from '@angular/router';
import { LanguageAdaptationComponent } from '../language-adaptation/language-adaptation.component';
import { AcousticAdaptationComponent } from '../acoustic-adaptation/acoustic-adaptation.component';
import { DictationComponent } from '../dictation/dictation.component';
import { SignUpComponent } from '../sign-up/sign-up.component';

const routes: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: '', redirectTo: '/sign-up', pathMatch: 'full' },
  { path: 'acoustic', component: AcousticAdaptationComponent },
  { path: 'language', component: LanguageAdaptationComponent },
  { path: 'dictation', component: DictationComponent },
  { path: 'sign-up/:id', component: AcousticAdaptationComponent }
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
