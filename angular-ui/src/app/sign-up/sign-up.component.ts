import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { DoCheck, KeyValueDiffers, KeyValueDiffer } from '@angular/core';
import { GoogleAuthService } from 'ng-gapi';
import GoogleUser = gapi.auth2.GoogleUser
import { MyCookieService } from '../cookie.service'

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})

export class SignUpComponent implements OnInit {
  SESSION_STORAGE_KEY: string;
  validToken: boolean
  messages: any;
  info: any;

  differ: KeyValueDiffer<string, any>;

  constructor(private differs: KeyValueDiffers, private apiService: ApiService, private googleAuth: GoogleAuthService, private cookieServ: MyCookieService) {
    this.differ = this.differs.find({}).create();
  }

  ngOnInit() {
    this.validToken = false
    this.SESSION_STORAGE_KEY = ""
  }

  getCurrCookie() {
    return this.cookieServ.getCookie()
  }

  ngDoCheck() {
    const change = this.differ.diff(this);
    if (change) {
      change.forEachChangedItem(item => {
        if (item['key'] === 'SESSION_STORAGE_KEY') {
          this.validToken = true;
          this.getInfo(this.getCurrCookie())
        }
      });
    }
  }


  getInfo(cookie: string): void {
    let body = new HttpParams().set('token', this.SESSION_STORAGE_KEY, ).set('cookie', cookie);
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    this.apiService.getInfoService(body, headers).subscribe((data) => {
      this.info = data;
    })
  }

  signIn() {
    this.googleAuth.getAuth()
      .subscribe((auth) => {
        auth.signIn().then(res => this.signInSuccessHandler(res)
        )
      });
  }

  getMessages() {
    let body = new HttpParams().set('token', this.SESSION_STORAGE_KEY).set('cookie', this.getCurrCookie());
    let headers: HttpHeaders = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');
    this.apiService.getMessagesService(body, headers).subscribe((data) => {
      this.messages = data;
    })
  }


  public getToken(): string {
    let token: string = sessionStorage.getItem('token');
    if (!token) {
      throw new Error("no token set , authentication required");
    }
    return sessionStorage.getItem('token');
  }



  private signInSuccessHandler(res: GoogleUser) {
    this.SESSION_STORAGE_KEY = res.getAuthResponse().access_token
    localStorage.setItem('token', this.SESSION_STORAGE_KEY)
  }

}
