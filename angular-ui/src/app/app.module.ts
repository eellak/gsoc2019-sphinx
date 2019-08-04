import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { MenuComponent } from './menu/menu.component';
import { LanguageAdaptationComponent } from './language-adaptation/language-adaptation.component';
import { AcousticAdaptationComponent } from './acoustic-adaptation/acoustic-adaptation.component';
import { DictationComponent } from './dictation/dictation.component';
import { RoutingModule } from './routing/routing.module';

@NgModule({
  declarations: [
    AppComponent,
    SignUpComponent,
    MenuComponent,
    LanguageAdaptationComponent,
    AcousticAdaptationComponent,
    DictationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RoutingModule,
    HttpClientModule
  ],
  providers: [ HttpClientModule],
  bootstrap: [AppComponent]
})
export class AppModule { }
