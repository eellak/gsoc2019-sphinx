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
import { LoaderComponent } from './loader/loader.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LoaderService } from './loader.service';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { LoaderInterceptor } from './loader.interceptor';
import { CookieService } from 'ngx-cookie-service';


@NgModule({
  declarations: [
    AppComponent,
    SignUpComponent,
    MenuComponent,
    LanguageAdaptationComponent,
    AcousticAdaptationComponent,
    DictationComponent,
    LoaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RoutingModule,
    HttpClientModule,
    MatProgressSpinnerModule
  ],
  providers: [CookieService, LoaderService, { provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true }],
  bootstrap: [AppComponent]
})
export class AppModule { }
