// Squares Background Animation (Your original perfect animation)
class SquaresBackground {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        this.direction = options.direction || 'diagonal';
        this.speed = options.speed || 0.5;
        this.borderColor = options.borderColor || 'rgba(65, 97, 139, 0.3)';
        this.squareSize = options.squareSize || 25;
        this.hoverFillColor = options.hoverFillColor || 'rgba(34, 34, 34, 0.2)';
        
        this.gridOffset = { x: 0, y: 0 };
        this.hoveredSquare = null;
        this.animationId = null;
        
        this.init();
    }
    
    init() {
        this.resizeCanvas();
        this.setupEventListeners();
        this.animate();
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    setupEventListeners() {
        window.addEventListener('resize', () => this.resizeCanvas());
        
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            const startX = Math.floor(this.gridOffset.x / this.squareSize) * this.squareSize;
            const startY = Math.floor(this.gridOffset.y / this.squareSize) * this.squareSize;
            
            const hoveredSquareX = Math.floor((mouseX + this.gridOffset.x - startX) / this.squareSize);
            const hoveredSquareY = Math.floor((mouseY + this.gridOffset.y - startY) / this.squareSize);
            
            this.hoveredSquare = { x: hoveredSquareX, y: hoveredSquareY };
        });
        
        this.canvas.addEventListener('mouseleave', () => {
            this.hoveredSquare = null;
        });
    }
    
    drawGrid() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        const startX = Math.floor(this.gridOffset.x / this.squareSize) * this.squareSize;
        const startY = Math.floor(this.gridOffset.y / this.squareSize) * this.squareSize;
        
        for (let x = startX; x < this.canvas.width + this.squareSize; x += this.squareSize) {
            for (let y = startY; y < this.canvas.height + this.squareSize; y += this.squareSize) {
                const squareX = x - (this.gridOffset.x % this.squareSize);
                const squareY = y - (this.gridOffset.y % this.squareSize);
                
                if (this.hoveredSquare &&
                    Math.floor((x - startX) / this.squareSize) === this.hoveredSquare.x &&
                    Math.floor((y - startY) / this.squareSize) === this.hoveredSquare.y) {
                    this.ctx.fillStyle = this.hoverFillColor;
                    this.ctx.fillRect(squareX, squareY, this.squareSize, this.squareSize);
                }
                
                this.ctx.strokeStyle = this.borderColor;
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(squareX, squareY, this.squareSize, this.squareSize);
            }
        }
    }
    
    updateAnimation() {
        const effectiveSpeed = Math.max(this.speed, 0.1);
        
        switch (this.direction) {
            case 'diagonal':
                this.gridOffset.x = (this.gridOffset.x - effectiveSpeed + this.squareSize) % this.squareSize;
                this.gridOffset.y = (this.gridOffset.y - effectiveSpeed + this.squareSize) % this.squareSize;
                break;
        }
    }
    
    animate() {
        this.updateAnimation();
        this.drawGrid();
        this.animationId = requestAnimationFrame(() => this.animate());
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SquaresBackground('squaresCanvas', {
        direction: 'diagonal',
        speed: 0.5,
        borderColor: 'rgba(65, 97, 139, 0.3)',
        squareSize: 25,
        hoverFillColor: 'rgba(34, 34, 34, 0.2)'
    });
});
