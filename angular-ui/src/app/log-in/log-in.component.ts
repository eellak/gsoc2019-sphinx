import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { GoogleAuthService } from 'ng-gapi';
import GoogleUser = gapi.auth2.GoogleUser
import { MyCookieService } from '../cookie.service'
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})

export class LogInComponent implements OnInit {

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

  signIn() {
    this.googleAuth.getAuth()
      .subscribe((auth) => {
        auth.signIn().then(res => this.signInSuccessHandler(res)
        )
      });
  }

  onSubmit(form: NgForm) {
    this.getMessages(form)
  }

  getMessages(form) {
    let body = new HttpParams().set('token', this.getAuthToken()).set('cookie', this.getCookie()).set('keep', form.value.keep);
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    headers = headers.append('Access-Control-Allow-Origin', '*');
    headers = headers.append("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    this.apiService.getMessagesService(body, headers).subscribe((data) => {
      sessionStorage.setItem('messages', JSON.stringify(data));
    })
  }


  private signInSuccessHandler(res: GoogleUser) {
    sessionStorage.setItem('token', res.getAuthResponse().access_token);
    window.location.reload();
  }

}
