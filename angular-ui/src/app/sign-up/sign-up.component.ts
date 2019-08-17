import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { GoogleAuthService } from 'ng-gapi';
import GoogleUser = gapi.auth2.GoogleUser
import { MyCookieService } from '../cookie.service'

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})

export class SignUpComponent implements OnInit {

  constructor(private apiService: ApiService, private googleAuth: GoogleAuthService, private cookieServ: MyCookieService) { }

  ngOnInit() { }

  getCookie() {
    return this.cookieServ.getCookie()
  }

  getAuthToken() {
    return sessionStorage.getItem('token')
  }


  getInfoSession() {
    return JSON.parse(sessionStorage.getItem('info'))
  }

  getMessagesSession() {
    return JSON.parse(sessionStorage.getItem('messages'))
  }


  getInfo(): void {
    let body = new HttpParams().set('token', this.getAuthToken()).set('cookie', this.getCookie());
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    this.apiService.getInfoService(body, headers).subscribe((data) => {
      sessionStorage.setItem('info', JSON.stringify(data));
    })
  }

  async signIn() {
    await this.googleAuth.getAuth()
      .subscribe((auth) => {
        auth.signIn().then(res => this.signInSuccessHandler(res)
        )
      });
  }

  getMessages() {
    console.log('2')
    let body = new HttpParams().set('token', this.getAuthToken()).set('cookie', this.getCookie());
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    this.apiService.getMessagesService(body, headers).subscribe((data) => {
      sessionStorage.setItem('messages', JSON.stringify(data));
    })
  }


  private signInSuccessHandler(res: GoogleUser) {
    sessionStorage.setItem('token', res.getAuthResponse().access_token);
  }

}
