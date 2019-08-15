import { Injectable, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';


@Injectable({
  providedIn: 'root'
})

export class MyCookieService {
  constructor(private cookieService: CookieService) {
    this.cookieService.set('cookie', Math.random().toString())
  }


  getCookie() {
    return this.cookieService.get('cookie')
  }

}
