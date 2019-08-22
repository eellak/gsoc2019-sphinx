import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LogInComponent } from './log-in/log-in.component';
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
import { OAuthModule } from 'angular-oauth2-oidc';
import {
  GoogleApiModule,
  NgGapiClientConfig,
  NG_GAPI_CONFIG,
} from "ng-gapi";
import { CommonModule } from '@angular/common';
import { MyCookieService } from './cookie.service';
import { FormsModule } from '@angular/forms';
import { Ng5SliderModule } from 'ng5-slider';
import { AudioRecordingService } from './recorder.service';
import { FooterComponent } from './footer/footer.component'

let gapiClientConfig: NgGapiClientConfig = {
  client_id: "301659838263-t8ddh4qm6308lqp8bhp7mehkdnfni6qp.apps.googleusercontent.com",
  discoveryDocs: ["https://accounts.google.com/.well-known/openid-configuration"],
  scope: "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
};

@NgModule({
  declarations: [
    AppComponent,
    LogInComponent,
    MenuComponent,
    LanguageAdaptationComponent,
    AcousticAdaptationComponent,
    DictationComponent,
    LoaderComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RoutingModule,
    HttpClientModule,
    MatProgressSpinnerModule,
    CommonModule,
    OAuthModule.forRoot(),
    GoogleApiModule.forRoot({
      provide: NG_GAPI_CONFIG,
      useValue: gapiClientConfig
    }),
    FormsModule,
    Ng5SliderModule
  ],
  providers: [CookieService, LoaderService, { provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true }, MyCookieService, AudioRecordingService],
  bootstrap: [AppComponent]
})
export class AppModule { }
