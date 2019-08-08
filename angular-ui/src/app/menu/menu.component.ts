import { Component, OnInit } from '@angular/core';
import { SignUpComponent } from '../sign-up/sign-up.component'

@Component({
  providers: [SignUpComponent],
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

  constructor(private signComp: SignUpComponent) { }

  ngOnInit() {
  }

}
